import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MenuComponent } from './Components/Menu/menu/menu.component';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgLetModule } from 'ng-let';
import { ButtonModule } from 'primeng/button';
import { DividerModule } from 'primeng/divider';
import { SidebarModule } from 'primeng/sidebar';
import { ToastModule } from 'primeng/toast';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { JwtInterceptor } from './jwt.interceptor';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';
import { TechniqueFormComponent } from './Components/Advices/Technique/technique-form/technique-form.component';
import { CustomInputComponent } from './Components/Generic/text-input/custom-input.component';
import { ErrorInterceptor } from './error.interceptor';
import { ObjectiveComponent } from './Components/Advices/Objectives/objective/objective.component';
import { ObjectiveFormComponent } from './Components/Advices/Objectives/objective-form/objective-form.component';
import { StageComponent } from './Components/Advices/Stages/stage/stage.component';
import { StageFormComponent } from './Components/Advices/Stages/stage-form/stage-form.component';
import { MultiSelectModule } from 'primeng/multiselect';
import { MarkdownModule } from 'ngx-markdown';

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    AuthenticationComponent,
    AdvicesComponent,
    TechniqueComponent,
    TechniqueFormComponent,
    CustomInputComponent,
    ObjectiveComponent,
    ObjectiveFormComponent,
    StageComponent,
    StageFormComponent,
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
