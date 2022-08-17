export const LOGIN = '/login' as const;
export const DEMO = '/demo' as const;

// patient routes
export const CHAT_WITH_ASSISTANT = '/chat' as const;

// assistant routes
export const PATIENTS = '/patients' as const;
export const CHAT_WITH_PATIENT = `${PATIENTS}/:id` as const;
