import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';

import {AccordionModule} from 'ngx-bootstrap/accordion';
import {ButtonsModule} from 'ngx-bootstrap/buttons';

import {SocketIoModule, SocketIoConfig} from 'ng2-socket-io';

import {AppComponent} from './app.component';
import {ThreadComponent} from './thread/thread.component';
import {KeysPipe} from './pipes/keys.pipe';
import {config} from "./config";
import {ThreadService} from "./thread/thread-service/thread.service";

const socketConfig: SocketIoConfig = config;

@NgModule({
  declarations: [
    AppComponent,
    ThreadComponent,
    KeysPipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AccordionModule.forRoot(),
    ButtonsModule.forRoot(),
    SocketIoModule.forRoot(socketConfig)
  ],
  providers: [ThreadService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
