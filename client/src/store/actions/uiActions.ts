import { Action } from './baseAction';
import * as ui from '../interfaces/ui';
import { ChatController } from 'chat-ui-react';

export namespace Type {
    export const ChangeMode = 'UI_CHANGE_MODE';
    export const ChangeInitMessage = 'UI_CHANGE_INIT_MSG';
    export const SaveAudio = 'UI_SAVE_AUDIO';
    export const SaveAnswerText = 'UI_SAVE_ANSWER_TEXT';
    export const ChangeAnswerWaiting = 'UI_CHANGE_ANSWER_WAITING';
    export const SaveChat = 'UI_SAVE_CHAT';
}

export function ChangeUIMode(mode: ui.Mode): Action<ui.Mode> {
    return {
        type: Type.ChangeMode,
        payload: mode,
    };
}

export function ChangeInitMessage(msg: string): Action<string> {
    return {
        type: Type.ChangeInitMessage,
        payload: msg,
    };
}

export function SaveAudio(url: string): Action<string> {
    return {
        type: Type.SaveAudio,
        payload: url,
    };
}

export function SaveAnswerText(answerText: string): Action<string> {
    return {
        type: Type.SaveAnswerText,
        payload: answerText,
    };
}

export function ChangeAnswerWaiting(answerWaiting: boolean): Action<boolean> {
    return {
        type: Type.ChangeAnswerWaiting,
        payload: answerWaiting,
    };
}

export function SaveChat(chat: ChatController): Action<ChatController> {
    return {
        type: Type.SaveChat,
        payload: chat,
    };
}
