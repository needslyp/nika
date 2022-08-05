import * as React from 'react';
import { connect } from 'react-redux';

export const ScgViewerImpl: React.FC<any> = () => {
    const url = 'http://localhost:8000/?sys_id=answer_structure&scg_structure_view_only=true';
    const scgViewerCssProp: React.CSSProperties = {
        width: '50%',
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

export const ScgViewer = connect()(ScgViewerImpl);
