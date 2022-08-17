import * as React from 'react';
import {SC_WEB_URL} from "@constants";

export const ScgViewer = () => {
    const url = SC_WEB_URL + '/?sys_id=answer_structure&scg_structure_view_only=true';
    const scgViewerCssProp: React.CSSProperties = {
        width: '100%',
        height: '200%',
        position: 'relative',
    };
    const iframeCssProp: React.CSSProperties = {
        width: '100%',
        height: '100%',
        position: 'relative',
    };

    return (
        <div className="scg-viewer" style={scgViewerCssProp}>
            <iframe src={url} style={iframeCssProp} id="frame" />
        </div>
    );
};
