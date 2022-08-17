import { nanoid } from 'nanoid';
import { ReactNode, useCallback, useMemo, useState } from 'react';
import { ToastContext } from './constants';
import { IToast, TToastComponent, IToastParams, TAddToastParams } from './model';

export const ToastProvider = ({ children }: { children: ReactNode }) => {
    const [toasts, setToasts] = useState<IToast[]>([]);

    const addToast = useCallback((component: TToastComponent, baseParams?: TAddToastParams) => {
        const params: IToastParams = {
            id: baseParams?.id || nanoid(5),
            duration: baseParams?.duration || 'infinity',
        };
        setToasts((prev) => [{ params, component }, ...prev]);
    }, []);

    const removeToast = useCallback((id: string) => {
        setToasts((prev) => prev.filter((prevToast) => prevToast.params.id !== id));
    }, []);

    const contextValue = useMemo(() => ({ toasts, addToast, removeToast }), [toasts, addToast, removeToast]);

    return <ToastContext.Provider value={contextValue}>{children}</ToastContext.Provider>;
};
