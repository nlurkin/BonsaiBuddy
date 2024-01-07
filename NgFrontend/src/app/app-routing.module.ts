import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';

const routes: Routes = [
  { path: 'login', component: AuthenticationComponent },
  {
    path: 'advices',
    component: AdvicesComponent,
    title: 'BonsaiBuddy - Techniques',
  },
  {
    path: 'advices/technique/:id',
    component: TechniqueComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
