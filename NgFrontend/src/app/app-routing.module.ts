import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TreeInfoComponent } from './Components/TreeInfo/tree-info/tree-info.component';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';
import { TechniqueFormComponent } from './Components/Advices/Technique/technique-form/technique-form.component';
import { AdminComponent } from './Components/Admin/admin/admin.component';
import { ObjectiveComponent } from './Components/Advices/Objectives/objective/objective.component';
import { ObjectiveFormComponent } from './Components/Advices/Objectives/objective-form/objective-form.component';
import { StageComponent } from './Components/Advices/Stages/stage/stage.component';
import { StageFormComponent } from './Components/Advices/Stages/stage-form/stage-form.component';
import {
  hasPermissionsGuard,
  hasRoleGuard,
  isLoggedInGuard,
} from './has-permissions.guard';
import { ProfileComponent } from './Components/Users/profile/profile.component';
import { ProfileFormComponent } from './Components/Users/profile-form/profile-form.component';
import { PasswordFormComponent } from './Components/Users/password-form/password-form.component';

const routes: Routes = [
  { path: 'login', component: AuthenticationComponent },
  {
    path: 'treeinfo',
    component: TreeInfoComponent,
    title: 'BonsaiBuddy - Tree Information',
  },
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
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'admin/technique/create',
    component: TechniqueFormComponent,
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'advices/objective/:id',
    component: ObjectiveComponent,
  },
  {
    path: 'advices/objective/:id/update',
    component: ObjectiveFormComponent,
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'admin/objective/create',
    component: ObjectiveFormComponent,
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'advices/stage/:id',
    component: StageComponent,
  },
  {
    path: 'advices/stage/:id/update',
    component: StageFormComponent,
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'admin/stage/create',
    component: StageFormComponent,
    canActivate: [hasPermissionsGuard],
    data: { permissions: 'BonsaiAdvice.change_content' },
  },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [isLoggedInGuard],
  },
  {
    path: 'profile/update',
    component: ProfileFormComponent,
    canActivate: [isLoggedInGuard],
  },
  {
    path: 'profile/password',
    component: PasswordFormComponent,
    canActivate: [isLoggedInGuard],
  },
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [isLoggedInGuard, hasRoleGuard],
    data: { roles: ['content_manager'] },
  },
  { path: '', redirectTo: '/treeinfo', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
