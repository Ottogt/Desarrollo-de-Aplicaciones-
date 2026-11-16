import { DecimalPipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonItem,
  IonInput,
  IonButton,
  IonNote,
  IonIcon,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { cashOutline, swapHorizontalOutline } from 'ionicons/icons';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [
    DecimalPipe,
    FormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonItem,
    IonInput,
    IonButton,
    IonNote,
    IonIcon,
  ],
})
export class HomePage {
  /** Tasa fija: 8 quetzales = 1 dólar */
  readonly tasaCambio = 8;
  cantidadQuetzales: number | null = null;
  resultadoDolares: number | null = null;

  constructor() {
    addIcons({ cashOutline, swapHorizontalOutline });
  }

  convertir(): void {
    const cantidad = Number(this.cantidadQuetzales);
    if (!Number.isFinite(cantidad) || cantidad < 0) {
      this.resultadoDolares = null;
      return;
    }
    this.resultadoDolares = cantidad / this.tasaCambio;
  }

  limpiar(): void {
    this.cantidadQuetzales = null;
    this.resultadoDolares = null;
  }
}
