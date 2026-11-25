import { AsyncPipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import {
  AlertController, IonBackButton, IonBadge, IonButton, IonButtons, IonCard,
  IonCardContent, IonCardHeader, IonCardTitle, IonCheckbox, IonContent, IonHeader,
  IonInput, IonItem, IonLabel, IonList, IonNote, IonProgressBar, IonText, IonTitle,
  IonToolbar,
} from '@ionic/angular';
import { BehaviorSubject, catchError, finalize, of, shareReplay, switchMap } from 'rxjs';

import { Microaccion } from '../core/modelos';
import { RetosApi, mensajeError } from '../core/retos-api.service';
import { hoyIso, fechaCorta } from '../core/semaforo';

@Component({
  selector: 'app-plan-rescate',
  imports: [
    AsyncPipe, ReactiveFormsModule, IonBackButton, IonBadge, IonButton, IonButtons,
    IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonCheckbox, IonContent,
    IonHeader, IonInput, IonItem, IonLabel, IonList, IonNote, IonProgressBar,
    IonText, IonTitle, IonToolbar,
  ],
  styles: `
    .metricas { display: flex; gap: 20px; flex-wrap: wrap; margin: 12px 0; }
    .metricas strong { display: block; font-size: 1.6rem; }
    .hecha { text-decoration: line-through; color: var(--ion-color-medium); }
    ion-checkbox { margin-right: 12px; }
    ion-progress-bar { margin: 12px 0; }
  `,
  template: `
    <ion-header><ion-toolbar color="primary">
      <ion-buttons slot="start"><ion-back-button defaultHref="/retos"></ion-back-button></ion-buttons>
      <ion-title>Plan de rescate semanal</ion-title>
    </ion-toolbar></ion-header>
    <ion-content class="ion-padding">
      @if (error()) { <ion-text color="danger"><p role="alert">{{ error() }}</p></ion-text> }
      @if (plan$ | async; as plan) {
        <ion-card>
          <ion-card-header><ion-card-title>{{ plan.reto_titulo }} · semana {{ plan.semana }}</ion-card-title></ion-card-header>
          <ion-card-content>
            @if (plan.editable) {
              <p>Divide lo que falta en pasos concretos antes del {{ fechaCorta(plan.fecha_fin) }}.</p>
              <div class="metricas">
                <span><strong>{{ plan.faltante }} %</strong>pendiente del reto semanal</span>
                <span><strong>{{ plan.meta_diaria }} puntos</strong>meta diaria sugerida</span>
                <span><strong>{{ plan.dias_restantes }}</strong>días, incluyendo hoy</span>
              </div>
              <ion-note>La meta distribuye los puntos pendientes entre los días disponibles; es una orientación.</ion-note>
            } @else {
              <ion-badge color="medium">Plan de solo lectura</ion-badge>
              <p>Solo puedes organizar y completar acciones durante la semana en curso.</p>
            }
            <p>{{ plan.completadas }} de {{ plan.total_acciones }} microacciones hechas · {{ plan.minutos_pendientes }} minutos pendientes</p>
            <ion-progress-bar [value]="plan.progreso_acciones / 100" color="success"></ion-progress-bar>
            @if (plan.vencidas) { <ion-text color="warning"><p>{{ plan.vencidas }} acción(es) pendiente(s) de días anteriores.</p></ion-text> }
            <ion-note>Marcar acciones no cambia automáticamente el porcentaje de la semana. Registra tu avance real en Seguimiento.</ion-note>
          </ion-card-content>
        </ion-card>

        @if (plan.editable) {
          <form [formGroup]="form" (ngSubmit)="agregar()">
            <h2>Mi siguiente paso</h2>
            <ion-list>
              <ion-item><ion-input label="Microacción" labelPlacement="stacked" placeholder="Ej.: Resolver dos ejercicios" formControlName="titulo" [maxlength]="160"></ion-input></ion-item>
              <ion-item><ion-input label="Fecha objetivo" labelPlacement="stacked" type="date" formControlName="fecha_objetivo" [min]="plan.hoy" [max]="plan.fecha_fin"></ion-input></ion-item>
              <ion-item><ion-input label="Minutos estimados" labelPlacement="stacked" type="number" formControlName="minutos_estimados" [min]="1" [max]="240"></ion-input></ion-item>
            </ion-list>
            <ion-button expand="block" type="submit" [disabled]="form.invalid || guardando()">Añadir al plan</ion-button>
          </form>
        }

        <h2>Microacciones de la semana</h2>
        <ion-list>
          @for (accion of plan.acciones; track accion.id) {
            <ion-item>
              <ion-checkbox slot="start" [attr.aria-label]="'Completar ' + accion.titulo" [checked]="accion.completada"
                [disabled]="!plan.editable || guardando()" (ionChange)="completar(accion, $any($event).detail.checked)"></ion-checkbox>
              <ion-label [class.hecha]="accion.completada">
                <h3>{{ accion.titulo }}</h3>
                <p>{{ fechaCorta(accion.fecha_objetivo) }} · {{ accion.minutos_estimados }} min</p>
                @if (accion.vencida) { <ion-badge color="warning">Pendiente de un día anterior</ion-badge> }
              </ion-label>
              @if (plan.editable) { <ion-button slot="end" fill="clear" color="danger" [disabled]="guardando()" (click)="eliminar(accion)">Eliminar</ion-button> }
            </ion-item>
          } @empty { <ion-item><ion-label>Aún no hay microacciones. Empieza con un paso pequeño y concreto.</ion-label></ion-item> }
        </ion-list>
      } @else {
        @if (!error()) { <p>Cargando el plan…</p> }
      }
    </ion-content>
  `,
})
export class PlanRescatePage {
  private readonly api = inject(RetosApi);
  private readonly alerta = inject(AlertController);
  private readonly id = Number(inject(ActivatedRoute).snapshot.paramMap.get('id'));
  private readonly recargar$ = new BehaviorSubject<void>(undefined);
  readonly error = signal('');
  readonly guardando = signal(false);
  readonly fechaCorta = fechaCorta;
  readonly plan$ = this.recargar$.pipe(
    switchMap(() => this.api.obtenerPlan(this.id).pipe(
      catchError((e) => { this.error.set(mensajeError(e)); return of(null); }),
    )),
    shareReplay({ bufferSize: 1, refCount: true }),
  );
  readonly form = new FormGroup({
    titulo: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.maxLength(160)] }),
    fecha_objetivo: new FormControl(hoyIso(), { nonNullable: true, validators: [Validators.required] }),
    minutos_estimados: new FormControl<number | string>(25, { nonNullable: true, validators: [Validators.required, Validators.min(1), Validators.max(240)] }),
  });

  ionViewWillEnter(): void { this.error.set(''); this.recargar$.next(); }

  agregar(): void {
    if (this.form.invalid || this.guardando()) return;
    this.error.set(''); this.guardando.set(true);
    const valor = this.form.getRawValue();
    this.api.crearMicroaccion({ ...valor, tarea: this.id, minutos_estimados: Number(valor.minutos_estimados) })
      .pipe(finalize(() => this.guardando.set(false)))
      .subscribe({
        next: () => { this.form.reset({ titulo: '', fecha_objetivo: hoyIso(), minutos_estimados: 25 }); this.recargar$.next(); },
        error: (e) => this.error.set(mensajeError(e)),
      });
  }

  completar(accion: Microaccion, completada: boolean): void {
    if (accion.completada === completada || this.guardando()) return;
    this.error.set(''); this.guardando.set(true);
    this.api.completarMicroaccion(accion.id, completada).pipe(finalize(() => this.guardando.set(false)))
      .subscribe({ next: () => this.recargar$.next(), error: (e) => this.error.set(mensajeError(e)) });
  }

  async eliminar(accion: Microaccion): Promise<void> {
    const aviso = await this.alerta.create({ header: 'Eliminar microacción', message: '¿Quieres quitar este paso del plan?', buttons: [{ text: 'Cancelar', role: 'cancel' }, { text: 'Eliminar', role: 'confirm' }] });
    await aviso.present();
    if ((await aviso.onDidDismiss()).role !== 'confirm') return;
    this.error.set(''); this.guardando.set(true);
    this.api.eliminarMicroaccion(accion.id).pipe(finalize(() => this.guardando.set(false)))
      .subscribe({ next: () => this.recargar$.next(), error: (e) => this.error.set(mensajeError(e)) });
  }
}
