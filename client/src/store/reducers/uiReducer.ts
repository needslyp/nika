import * as ui from '../interfaces/ui';
import { Action } from '../actions/baseAction';
import * as uiAction from '../actions/uiActions';

export function reducer(state: ui.State = ui._initState, action: Action<any>): any {
    switch (action.type) {
        case uiAction.Type.ChangeMode:
            return { ...state, mode: action.payload };

        case uiAction.Type.ChangeInitMessage:
            return { ...state, initMessage: action.payload };

        case uiAction.Type.SaveAudio:
            return { ...state, url: action.payload };

        case uiAction.Type.SaveAnswerText:
            return { ...state, answerText: action.payload };

        case uiAction.Type.ChangeAnswerWaiting:
            return { ...state, answerWaiting: action.payload };

        case uiAction.Type.SaveChat:
            return { ...state, chat: action.payload };

        default:
            return state;
    }
}
