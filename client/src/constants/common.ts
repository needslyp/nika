const defaultSocketUrl = 'ws://localhost:8090';
const defaultScUrl = 'ws://localhost:8090';
<<<<<<< HEAD
const defaultScScWebUrl = 'http://localhost:8000'
=======
>>>>>>> 92191d324... feat(interface): remake static

export const SocketActions = {
    REQUEST_START_CALL: 'request-start-call',
    RESET_CALL: 'reset-call',
    CANDIDATE: 'candidate',
    OFFER: 'offer',
    ANSWER: 'answer',
};

export const SC_URL = process.env.SC_URL ?? defaultScUrl;
export const SOCKET_URL = process.env.SOCKET_URL ?? defaultSocketUrl;
<<<<<<< HEAD
export const SC_WEB_URL = process.env.SC_WEB_URL ?? defaultScScWebUrl;
=======
>>>>>>> 92191d324... feat(interface): remake static
