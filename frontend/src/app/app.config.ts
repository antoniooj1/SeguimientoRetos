import { provideIonicAngular } from '@ionic/angular';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideIonicAngular(),
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes)
  ]
};
