import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgLetModule } from 'ng-let';
import { MarkdownModule } from 'ngx-markdown';
import { ButtonModule } from 'primeng/button';
import { DividerModule } from 'primeng/divider';
import { MultiSelectModule } from 'primeng/multiselect';
import { SidebarModule } from 'primeng/sidebar';
import { ToastModule } from 'primeng/toast';
import { DropdownModule } from 'primeng/dropdown';
import { AdminComponent } from './Components/Admin/admin/admin.component';
import { ObjectiveFormComponent } from './Components/Advices/Objectives/objective-form/objective-form.component';
import { ObjectiveComponent } from './Components/Advices/Objectives/objective/objective.component';
import { StageFormComponent } from './Components/Advices/Stages/stage-form/stage-form.component';
import { StageComponent } from './Components/Advices/Stages/stage/stage.component';
import { TechniqueFormComponent } from './Components/Advices/Technique/technique-form/technique-form.component';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { CustomInputComponent } from './Components/Generic/text-input/custom-input.component';
import { MenuComponent } from './Components/Menu/menu/menu.component';
import { TreeInfoComponent } from './Components/TreeInfo/tree-info/tree-info.component';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { PasswordFormComponent } from './Components/Users/password-form/password-form.component';
import { ProfileFormComponent } from './Components/Users/profile-form/profile-form.component';
import { ProfileComponent } from './Components/Users/profile/profile.component';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CountryPipe } from './country.pipe';
import { ErrorInterceptor } from './error.interceptor';
import { JwtInterceptor } from './jwt.interceptor';
import { MyTreesComponent } from './Components/Users/my-trees/my-trees.component';

@NgModule({
  declarations: [
    AppComponent,
    TreeInfoComponent,
    MenuComponent,
    AuthenticationComponent,
    AdvicesComponent,
    TechniqueComponent,
    TechniqueFormComponent,
    CustomInputComponent,
    AdminComponent,
    ObjectiveComponent,
    ObjectiveFormComponent,
    StageComponent,
    StageFormComponent,
    ProfileComponent,
    ProfileFormComponent,
    CountryPipe,
    PasswordFormComponent,
    MyTreesComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ButtonModule,
    DividerModule,
    FormsModule,
    ReactiveFormsModule,
    SidebarModule,
    NgLetModule,
    ToastModule,
    MultiSelectModule,
    MarkdownModule.forRoot(),
    DropdownModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: JwtInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
