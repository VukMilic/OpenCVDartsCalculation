import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SlikaHsvComponent } from './slika-hsv/slika-hsv.component';
import { X01Component } from './x01/x01.component';
import { ClockComponent } from './clock/clock.component';

const routes: Routes = [
  {path: '', component: SlikaHsvComponent},
  {path: 'slika', component: SlikaHsvComponent},
  {path: 'x01', component: X01Component},
  {path: 'clock', component: ClockComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
