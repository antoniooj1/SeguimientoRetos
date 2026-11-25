import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'retos', pathMatch: 'full' },
  {
    path: 'semanas/:id/plan',
    loadComponent: () => import('./paginas/plan-rescate.page').then((m) => m.PlanRescatePage),
  },
  {
    path: 'retos',
    loadComponent: () => import('./paginas/retos-lista.page').then((m) => m.RetosListaPage),
  },
  {
    path: 'retos/nuevo',
    loadComponent: () => import('./paginas/reto-form.page').then((m) => m.RetoFormPage),
  },
  {
    path: 'retos/:id',
    loadComponent: () => import('./paginas/reto-detalle.page').then((m) => m.RetoDetallePage),
  },
  {
    path: 'alertas',
    loadComponent: () => import('./paginas/alertas.page').then((m) => m.AlertasPage),
  },
  { path: '**', redirectTo: 'retos' },
];
