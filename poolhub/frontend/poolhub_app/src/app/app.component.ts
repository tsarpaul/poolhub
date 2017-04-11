import {Component, OnInit} from '@angular/core';
import {Thread} from "./thread/thread";
import {Socket} from 'ng2-socket-io';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Pool dip';
  threads: {[ident: number]: Thread} = {};

  constructor(private socket: Socket) {

  }


  sortThreadsJsonRecursively(threads) {
    let ordered_threads = {};
    Object.keys(threads).sort().forEach(key => {
      ordered_threads[key] = threads[key];
    });
    for (let ident of Object.keys(ordered_threads)) {
      ordered_threads[ident]['children'] = this.sortThreadsJsonRecursively(ordered_threads[ident]['children']);
    }
    return ordered_threads;
  }

  ngOnInit() {
    this.pollUpdate();
    this.socket.on('reply', data => {
      let threads = data['threads'];
      let ordered_threads = this.sortThreadsJsonRecursively(threads);
      Thread.updateChildren(this.threads, ordered_threads);
    });
    this.socket.on('disconnect', () => {
      Object.keys(this.threads).forEach(ident => {
        this.threads[ident].killRecursively();
      });
    });
  }

  async pollUpdate() {
    await this.socket.emit('update', {'hello': 'world'}, () => {
      this.delay(this.pollUpdate.bind(this));
    });
  }

  timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async delay(fn, ...args) {
    await this.timeout(100);
    return fn(...args);
  }
}
