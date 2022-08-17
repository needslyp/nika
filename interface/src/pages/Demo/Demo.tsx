import { useCallback, useEffect, useState, Fragment } from 'react';
import { Wrapper, ChatWrapper, SCgViewerWrapper } from "./styled";
import { Message } from '@components/Chat/Message';
import { Chat } from '@components/Chat';
import { Date } from '@components/Chat/Date';
import { ScAddr } from 'ts-sc-client';
import { resolveUserAgent } from '@agents/resolveUserAgent';
import { useChat } from '@hooks/useChat';
import * as React from "react";
import { SC_WEB_URL } from "@constants";

export const Demo = () => {
    const [patient, setPatient] = useState<ScAddr | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const { initChat, sendMessage, isAgentAnswer, onFetching, messages, chatRef } = useChat(patient);
    const onSend = useCallback(
        async (text: string) => {
            if (!patient) return;
            await sendMessage(patient, text);
        },
        [patient, sendMessage],
    );

    const url = SC_WEB_URL + '/?sys_id=answer_structure&scg_structure_view_only=true';

    useEffect(() => {
        (async () => {
            const patient = await resolveUserAgent();
            if (!patient) return;
            setPatient(patient);
            await initChat([patient]);
            setIsLoading(false);
        })();
    }, [initChat]);

    return (
        <Wrapper>
            <ChatWrapper>
                <Chat
                    ref={chatRef}
                    isLoading={isLoading}
                    onSend={onSend}
                    onFetching={onFetching}
                    isAgentAnswer={isAgentAnswer}
                >
                    {messages.map((item, ind) => {
                        const prevItem = messages[ind - 1];
                        const showDate = item.date !== prevItem?.date;
                        return (
                            <Fragment key={item.id}>
                                {showDate && <Date date={item.date} />}
                                <Message
                                    isLeft={!!patient && !item.author.equal(patient)}
                                    time={item.time}
                                    attachment={item.attachment}
                                    isLoading={item.isLoading}
                                >
                                    {item.text}
                                </Message>
                            </Fragment>
                        );
                    })}
                </Chat>
            </ChatWrapper>
            <SCgViewerWrapper>
                <iframe src={url} style={{width: '100%', height: '100%', border: 0, borderRadius: '15px'}}/>
            </SCgViewerWrapper>
        </Wrapper>
    );
};
