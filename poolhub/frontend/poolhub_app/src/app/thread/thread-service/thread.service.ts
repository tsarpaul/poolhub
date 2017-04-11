import {Injectable} from '@angular/core';
import {Http} from "@angular/http";
import {config} from "../../config";

@Injectable()
export class ThreadService {

  constructor(private http: Http) {
  }

  terminateThread(ident) {
    return this.http.put(config.url + "/terminateThread", {ident: ident});
  }

}
