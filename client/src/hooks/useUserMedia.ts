import { useEffect, useState } from 'react';

const defaultConstrains = { audio: true, video: true };

export interface IError {
    name: string;
    message: string;
}

export const useUserMedia = (constraints: MediaStreamConstraints = defaultConstrains) => {
    const [stream, setStream] = useState<MediaStream | undefined>();
    const [error, setError] = useState<IError | undefined>();

    useEffect(() => {
        (async () => {
            try {
                const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
                setStream(mediaStream);
            } catch (e: any) {
                if (!e?.name) return;
                setError({ name: e.name, message: e.message });
            }
        })();
    }, [constraints]);

    return [stream, error] as const;
};
