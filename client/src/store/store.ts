<<<<<<< HEAD
import { net, serv, ui } from './interfaces';

export interface Store {
    net: net.State;
    services: serv.Services;
    ui: ui.State;
}

export const storeInitialState: Store = {
    net: net.State.Disconnected,
    services: serv._initServices,
    ui: ui._initState,
};
=======
import { configureStore } from '@reduxjs/toolkit';
import { profileSlice } from './profileSlice';
import { commonSlice } from './commonSlice';

export const store = configureStore({
    reducer: {
        [profileSlice.name]: profileSlice.reducer,
        [commonSlice.name]: commonSlice.reducer,
    },
});
>>>>>>> 92191d324... feat(interface): remake static
