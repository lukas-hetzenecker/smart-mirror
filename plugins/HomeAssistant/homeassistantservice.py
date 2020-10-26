import logging
import asyncio
import websockets
import json
import ssl
import collections

from PySide2.QtCore import Property, Signal, Slot, QObject

logger = logging.getLogger(__name__)


class HomeAssistantService(QObject):
    hostnameChanged = Signal(str)
    portChanged = Signal(int)
    secureChanged = Signal(bool)
    accessTokenChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hostname = "localhost"
        self._port = 8123
        self._secure = False
        self._access_token = ''
        self._websocket = None
        self._lastId = 0

        self._states = {}
        self._state_listeners = collections.defaultdict(list)

    def getHostname(self):
        return self._hostname

    def setHostname(self, hostname):
        self._hostname = hostname
        self.hostnameChanged.emit(self._hostname)

    hostname = Property(str, getHostname, setHostname, notify=hostnameChanged)

    def getPort(self):
        return self._port

    def setPort(self, port):
        self._port = port
        self.portChanged.emit(self._port)

    port = Property(int, getPort, setPort, notify=portChanged)

    def getSecure(self):
        return self._secure

    def setSecure(self, secure):
        self._secure = secure
        self.secureChanged.emit(self._secure)

    secure = Property(bool, getSecure, setSecure, notify=secureChanged)

    def getAccessToken(self):
        return self._access_token

    def setAccessToken(self, access_token):
        self._access_token = access_token
        self.accessTokenChanged.emit(self._access_token)

    accessToken = Property(str, getAccessToken, setAccessToken, notify=accessTokenChanged)

    @Slot()
    def start(self):
        asyncio.ensure_future(self._start())

    @Slot(str, str, 'QVariantMap')
    def callService(self, domain, service, service_data={}):
        self._lastId += 1
        asyncio.ensure_future(self._websocket.send(json.dumps({
            'id': self._lastId,
            'type': 'call_service',
            'domain': domain,
            'service': service,
            'service_data': service_data
        })))

    def add_state_listener(self, entity_id, listener):
        self._state_listeners[entity_id].append(listener)
        return self._states.get(entity_id, {})

    def remove_state_listener(self, entity_id, listener):
        self._state_listeners[entity_id].remove(listener)

    def _update_state(self, entity_id, state):
        self._states[entity_id] = state
        for listener in self._state_listeners[entity_id]:
            listener(state)

    async def _start(self):
        SUBSCRIBE_EVENTS_ID = 1
        GET_STATES_ID = 2

        try:
            url = '%s://%s:%s/api/websocket' % (
                'wss' if self._secure else 'ws', self._hostname, self._port)

            logger.debug('Connecting to home-assistant websocket %s...', url)

            self._websocket = await websockets.connect(url)

            logger.debug('Connected to home-assistant websocket')

            auth_message = await self._websocket.recv()
            logger.debug(auth_message)

            if self._access_token:
                await self._websocket.send(json.dumps({'type': 'auth', 'access_token': self._access_token}))
                auth_message = await self._websocket.recv()
                logger.debug(auth_message)

            await self._websocket.send(json.dumps({'id': SUBSCRIBE_EVENTS_ID, 'type': 'subscribe_events', 'event_type': 'state_changed'}))
            await self._websocket.send(json.dumps({'id': GET_STATES_ID, 'type': 'get_states'}))
            self._lastId = GET_STATES_ID

            while True:
                data = await self._websocket.recv()
                if not data:
                    break
                message = json.loads(data)
                #logger.debug(message)
                if message['id'] == GET_STATES_ID:
                    for state in message['result']:
                        self._update_state(state['entity_id'], state)
                elif message['type'] == 'event':
                    event = message['event']
                    if event['event_type'] == 'state_changed':
                        entity_id = event['data']['entity_id']
                        new_state = event['data']['new_state']
                        self._update_state(entity_id, new_state)
        except Exception as e:
            logger.error(e)
            
        await asyncio.sleep(10.0)
        await self._start()


class HomeAssistantStateListener(QObject):
    entityIdChanged = Signal(str)
    connectionChanged = Signal(HomeAssistantService)
    stateChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._entityId = None
        self._connection = None
        self._state = {}

    def getEntityId(self):
        return self._entityId

    def setEntityId(self, entityId):
        print("entityId is now", entityId, "_connection", self._connection)
        if self._connection is not None and self._entityId is not None:
            self._connection.remove_state_listener(self._entityId)

        self._entityId = entityId
        self.entityIdChanged.emit(self._entityId)

        if self._connection is not None:
            state = self._connection.add_state_listener(entityId, self._update)
            self._update(state)

    entityId = Property(str, getEntityId, setEntityId, notify=entityIdChanged)

    def getConnection(self):
        return self._entityId

    def setConnection(self, connection):
        print("connection is now", connection, "_entityId", self._entityId)
        self._connection = connection
        self.connectionChanged.emit(connection)

        if self._entityId is not None:
            state = self._connection.add_state_listener(self._entityId, self._update)
            self._update(state)

    connection = Property(HomeAssistantService, getConnection, setConnection, notify=connectionChanged)

    def getState(self):
        return self._state.get('state', 'unknown')
 
    state = Property(str, getState, notify=stateChanged)

    def getAttributes(self):
        return self._state.get('attributes', {})

    attributes = Property('QVariantMap', getAttributes)

    def getNames(self):
        faces = self._state.get('attributes', {}).get('faces', [])
        names = []
        for face in faces:
            names.append(face['name'])
        return names

    names = Property('QVariant', getNames)


    def _update(self, state):
        self._state = state
        self.stateChanged.emit(self.state)
