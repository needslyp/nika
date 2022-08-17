import { ExtractRouteParams } from 'react-router';
import { generatePath, useHistory } from 'react-router-dom';
import { useCallback } from 'react';

export const useNavigation = <Url extends string>(url: Url, params?: ExtractRouteParams<Url>) => {
    const history = useHistory();

    return useCallback(() => {
        history.push(generatePath(url, params));
    }, [history, params, url]);
};

type UseParamReturn<Hole extends Record<string, any>, Given extends Record<string, any> | undefined> = (
    props: Omit<Hole, keyof Given>,
) => () => void;

export const useParamNavigation = <Url extends string, Params extends Partial<ExtractRouteParams<Url>> | undefined>(
    url: Url,
    params?: Params,
): UseParamReturn<ExtractRouteParams<Url>, Params> => {
    const history = useHistory();

    return useCallback(
        (addParams) => () =>
            history.push(
                generatePath(url, {
                    ...params,
                    ...addParams,
                } as unknown as ExtractRouteParams<Url>),
            ),
        [history, params, url],
    );
};
