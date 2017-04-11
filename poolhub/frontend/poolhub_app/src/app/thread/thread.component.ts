import {Component, OnInit, Input, KeyValueDiffers, ChangeDetectorRef, DoCheck} from '@angular/core';
import {Thread} from "./thread";
import {ThreadService} from "./thread-service/thread.service";

@Component({
  selector: 'app-thread',
  templateUrl: './thread.component.html',
  styles: [require('./thread.component.css')]
})
export class ThreadComponent implements OnInit, DoCheck {
  @Input() threads: Array<Thread>;
  @Input() accordionOpenOnStart: boolean = false;
  objDiffers: any;

  constructor(private differs: KeyValueDiffers, private changeDetectorRef: ChangeDetectorRef,
              private threadService: ThreadService) {
    this.objDiffers = differs.find({}).create(null);
  }

  ngOnInit() {
  }

  shouldTerminateButton(thread){
    const nonTerminableThreads = ['MainThread', 'PoolHub Server', 'PoolHub Watcher'];
    // Make sure thread alive and not non-terminable
    return thread.health === 'Alive' && nonTerminableThreads.indexOf(thread.name) == -1;
  }

  isThreadAlive(thread: Thread) {
    let health = thread.health;
    return health === 'Alive' ? 'panel-success' : 'panel-danger';
  }

  ngDoCheck() {
    let changes = this.objDiffers.diff(this.threads);
    if (changes) {
      this.changeDetectorRef.markForCheck();
    }
  }

  terminateThread(thread: Thread) {
    this.threadService.terminateThread(thread.ident).subscribe(() => {});
  }
}
