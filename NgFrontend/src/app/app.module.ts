import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MenuComponent } from './Components/Menu/menu/menu.component';
import { NgLetDirective } from './Directives/ng-let.directive';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { DividerModule } from 'primeng/divider';
import { SidebarModule } from 'primeng/sidebar';
import { AdvicesComponent } from './Components/Advices/advices.component';
import { AuthenticationComponent } from './Components/Users/authentication/authentication.component';
import { JwtInterceptor } from './jwt.interceptor';
import { TechniqueComponent } from './Components/Advices/Technique/technique/technique.component';

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    NgLetDirective,
    AuthenticationComponent,
    AdvicesComponent,
    TechniqueComponent,
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
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: JwtInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
