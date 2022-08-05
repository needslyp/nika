import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { Button, Tooltip } from 'antd';
import { StereoAudioRecorder } from 'recordrtc';
import * as store from '../store';
import { connect } from 'react-redux';
import { ScAddr } from '@ostis/sc-core';
import { ChatController, MuiChat } from 'chat-ui-react';
import { ButtonPlacementChat } from './ButtonPlacementChat';
import { FileExcelOutlined, SoundOutlined } from '@ant-design/icons';
import RecordRTC = require('recordrtc');

interface Recorder {
    startRecording();

    stopRecording(callback: () => void);

    playSoundContent(soundContent: string);

    getBlob();

    getDataURL();

    destroy();

    state: string;
}

export interface ButtonPlacementChatProps {
    inputRef?: any;
    inputValue?: string;
    onChange?: (e: any) => void;
    enterMessage?: (e: any) => void;
    sendInputText?: (e: any) => void;
    widgetAudioButton?: string;
    startRecording?: (e: any) => void;
    outlinedType?: string;
    className?: string;
}

export interface KnowledgeBaseProps {
    services: store.serv.Services;
    url: string;
    answerText: string;
    answerWaiting: boolean;
    chat: ChatController;
}

function mapStateToProps(state: store.Store): KnowledgeBaseProps {
    return {
        services: state.services,
        url: state.ui.url,
        answerText: state.ui.answerText,
        answerWaiting: state.ui.answerWaiting,
        chat: state.ui.chat,
    };
}

export const VoiceRecorderImpl: React.FC<KnowledgeBaseProps> = (props: KnowledgeBaseProps) => {
    const microphone = useRef<MediaStream | null>(null);
    const recorder = useRef<Recorder | null>(null);
    const audioEl = useRef<HTMLAudioElement | null>(null);
    const [recordingStarted, setRecordingStarted] = useState<boolean>(false);
    const [tipClicked, setTipClicked] = useState<boolean>(false);
    const { services } = props;
    const chatController = props.chat;
    const [inputValue, setInputValue] = useState('');
    const [lastInputValue, setLastInputValue] = useState('');
    const [sendedUserMessage, setSendedUserMessage] = useState(false);
    const [cursorLocation, setCursorLocation] = useState(0);
    const [audioIsPlayed, setAudioIsPlayed] = useState(false);

    const messageButtonStyles: React.CSSProperties = {
        flex: '1 0 0%',
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        border: '0px',
        color: 'rgb(138,168,246)',
        borderRadius: '50%',
        margin: '0px 0px 5px 10px',
        height: '35px',
        width: '35px',
        boxShadow: '1px 1px 2px rgba(0,0,0,.3)',
    };
    const messageIconStyles: React.CSSProperties = { margin: '3px', fontSize: '20px' };

    const MINIMAL_DESKTOP_WIDTH = 800;
    const [isDesktop, setIsDesktop] = useState(window.innerWidth >= MINIMAL_DESKTOP_WIDTH);

    useEffect(() => {
        const proms = document.getElementsByClassName('prom-1');
        for (const prom of proms) {
            prom.addEventListener('click', (e) => {
                const target = e.target as HTMLDivElement;
                const inputValue = target.innerText;
                setCursorLocation(inputValue.length);
                setTipClicked(true);
                setInputValue(inputValue);
                setTipClicked(false);
            });
        }
    }, []);

    const getMicPermission = async () => {
        if (microphone.current) {
            return microphone.current;
        }

        if (!navigator || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("This browser doesn't supports getUserMedia API.");
            if ((navigator as any).getUserMedia) {
                console.log('This browser uses deprecated getUserMedia API.');
            }

            throw new Error("can't use VoiceRecorder Component");
        }

        try {
            return await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: false,
                },
            });
        } catch (error) {
            alert('Unable to capture your microphone.');
            throw error;
        }
    };

    const startRecording = async (e: React.MouseEvent) => {
        e.preventDefault();
        if (!recordingStarted) {
            if (!microphone.current) {
                microphone.current = await getMicPermission();
            }

            if (audioEl.current) {
                audioEl.current.muted = true;
                audioEl.current.srcObject = microphone.current;
            }

            if (recorder.current) {
                recorder.current.destroy();
                recorder.current = null;
            }

            recorder.current = RecordRTC(microphone.current, {
                type: 'audio',
                mimeType: 'audio/wav',
                recorderType: StereoAudioRecorder,
                desiredSampRate: 16000,
                bufferSize: 1024,
                numberOfAudioChannels: 1,
            });

            setRecordingStarted(true);
        } else {
            setRecordingStarted(false);
        }
    };

    const playSoundContent = (soundContent: string) => {
        if (soundContent && !audioIsPlayed) {
            setAudioIsPlayed(true);
            const sound = new Audio('data:audio/wav;base64,' + soundContent);
            sound.play().then(() => setAudioIsPlayed(false));
        }
    };


    const processSystemReplyMessage = (replyMessageAddr) => {
        Promise.all([
            services.sc.utils.findMessageLinkContent(replyMessageAddr, services.sc.keynodes.kConceptTextFile),
            services.sc.utils.findMessageLinkContent(replyMessageAddr, services.sc.keynodes.kConceptSoundFile),
        ])
            .then(([replyText, replySoundText]) => {
                services.sc.saveAnswerText(replyText);
                if (replySoundText != null) {
                    playSoundContent(replySoundText);
                }
                const audioButton = (
                    <Button
                        icon={<SoundOutlined className={'soundOutlined'} style={messageIconStyles} />}
                        style={messageButtonStyles}
                        onClick={() => playSoundContent(replySoundText)}
                        key={0}
                    />
                );

                return chatController.addMessage({
                    type: 'text',
                    content: replyText,
                    self: false,
                    buttons: [audioButton],
                });
            })
            .then(() => {
                services.sc.saveChat(chatController);
                services.sc.changeAnswerWaiting(false);
            });
    };

    const waitSystemReplyMessage = async (actionNode: ScAddr) => {
        const onActionFinished = () => {
            services.sc.utils
                .findSystemReplyMessage(actionNode)
                .then((replyMessageAddr) => processSystemReplyMessage(replyMessageAddr));
        };
        services.sc.utils.waitActionFinish(actionNode, onActionFinished);
    };

    const CustomRecorderButtonForChat = () => {
        const inputRef = useRef();
        useEffect(() => {
            (inputRef.current as any).focus();
            (inputRef.current as any).selectionStart = cursorLocation;
            (inputRef.current as any).selectionEnd = cursorLocation;
        }, [inputRef]);

        const onChange = (e) => {
            setInputValue(e.target.value);
            setCursorLocation(e.target.selectionStart);
        };

        const enterMessage = (event: any) => {
            const enterButton = event.which || event.keyCode;
            if (enterButton == 13) {
                sendInputText(event);
            } else if (enterButton == '38') {
                setInputValue(lastInputValue);
            }
        };

        const sendInputText = async (e: React.MouseEvent) => {
            e.preventDefault();
            if (inputValue != '') {
                services.sc.changeAnswerWaiting(true);
                setLastInputValue(inputValue);
                await chatController.addMessage({
                    type: 'text',
                    content: inputValue,
                    self: true,
                });
                services.sc.saveChat(chatController);
                setInputValue('');
                setSendedUserMessage(!sendedUserMessage);

                const actionNode: ScAddr = await services.sc.utils.InitMessageReplyAction(inputValue, false);
                return waitSystemReplyMessage(actionNode);
            }
        };

        const props = {
            inputRef,
            inputValue,
            onChange,
            enterMessage,
            sendInputText,
            startRecording,
            widgetAudioButton: recordingStarted ? 'recording-button animate-pulse' : 'recording-button',
            outlinedType: recordingStarted ? 'BorderOutlined' : 'AudioOutlined',
            className: tipClicked ? 'user-message-input animate-pulse-input' : 'user-message-input',
        };

        return <ButtonPlacementChat {...props} />;
    };

    const handleScreenResize = () => {
        setIsDesktop(window.innerWidth >= MINIMAL_DESKTOP_WIDTH);
    };

    useEffect(() => {
        window.addEventListener('resize', handleScreenResize);
        chatController.setActionRequest({
            type: 'custom',
            Component: CustomRecorderButtonForChat,
        });
        services.sc.saveChat(chatController);
        if (recordingStarted && microphone.current) {
            if (recorder.current) {
                recorder.current.startRecording();
            }
        } else if (!recordingStarted && microphone.current && recorder.current) {
            if (recorder.current.state === 'recording') {
                if (recorder.current) {
                    services.sc.changeAnswerWaiting(true);
                    recorder.current.stopRecording(async () => {
                        const recordedBlob: Blob = recorder.current.getBlob();
                        const recordedBlobText: string = await services.sc.utils.blobToBase64(recordedBlob);
                        URL.createObjectURL(recordedBlob);
                        services.sc.saveAudio(recordedBlobText);
                        const actionNode: ScAddr = await services.sc.utils.InitMessageReplyAction(
                            recordedBlobText,
                            true,
                        );
                        const messageNode: ScAddr = await services.sc.userMessageController.findUserMessageNode(
                            actionNode,
                        );
                        const userMessageContent = await services.sc.userMessageController.findUserText(messageNode);
                        await chatController.addMessage({
                            type: 'text',
                            content: userMessageContent,
                            self: true,
                        });
                        services.sc.saveChat(chatController);
                        return waitSystemReplyMessage(actionNode);
                    });
                }
            } else if (recordingStarted) {
                console.log('Unable to capture your microphone');
            }
        }
    }, [recordingStarted, microphone, recorder, inputValue]);

    return (
        <div className="chat-widget-container">
            <div className="chat-widget">
                {!props.answerWaiting && <div className="chat-widget-header" />}
                {props.answerWaiting && (
                    <div className="chat-widget-header">
                        <div className="dot" />
                        <div className="dot" />
                        <div className="dot" />
                        <div className="dot" />
                        <div className="dot" />
                    </div>
                )}
                <div className="chat-widget-content">
                    <Tooltip
                        title={
                            recordingStarted
                                ? 'Click on the button to stop recording'
                                : 'Click on the button to start recording'
                        }
                    >
                        <MuiChat chatController={props.chat} />
                    </Tooltip>
                </div>
            </div>
        </div>
    );
};

export const VoiceRecorder = connect(mapStateToProps)(VoiceRecorderImpl);
