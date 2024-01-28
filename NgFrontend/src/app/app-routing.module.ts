import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';
import { TechniqueFormComponent } from './Components/Advices/Technique/technique-form/technique-form.component';
import { ObjectiveComponent } from './Components/Advices/Objectives/objective/objective.component';
import { ObjectiveFormComponent } from './Components/Advices/Objectives/objective-form/objective-form.component';
import { StageComponent } from './Components/Advices/Stages/stage/stage.component';
import { StageFormComponent } from './Components/Advices/Stages/stage-form/stage-form.component';

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
  {
    path: 'advices/technique/:id/update',
    component: TechniqueFormComponent,
  },
  {
    path: 'admin/technique/create',
    component: TechniqueFormComponent,
  },
  {
    path: 'advices/objective/:id',
    component: ObjectiveComponent,
  },
  {
    path: 'advices/objective/:id/update',
    component: ObjectiveFormComponent,
  },
  {
    path: 'admin/objective/create',
    component: ObjectiveFormComponent,
  },
  {
    path: 'advices/stage/:id',
    component: StageComponent,
  },
  {
    path: 'advices/stage/:id/update',
    component: StageFormComponent,
  },
  {
    path: 'admin/stage/create',
    component: StageFormComponent,
  },
  { path: '', redirectTo: '/treeinfo', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
