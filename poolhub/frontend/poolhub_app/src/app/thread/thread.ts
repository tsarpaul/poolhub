export class Thread {
  ident: number;
  name: string;
  health: string;
  status: string;
  exception: string;
  daemon: boolean;
  last_updated: number;
  children: {[ident: number]: Thread} = {};

  constructor(thread: Object) {
    this.update(thread);
  }

  update(thread: Object) {
    this.ident = thread['ident'];
    this.name = thread['name'];
    this.health = thread['health'];
    this.status = thread['status'];
    this.exception = thread['exception'];
    this.daemon = thread['daemon'];
    this.last_updated = parseInt(thread['updated'].split(".")[0]);
    Thread.updateChildren(this.children, thread['children']);
  }

  static updateChildren(threads_to_update: {[ident: number]: Thread}, threads: {[ident: number]: Object}) {
    Object.keys(threads).forEach(ident => {
      let thread = threads[ident];
      if (Object.keys(threads_to_update).indexOf(ident) > -1) {
        threads_to_update[ident].update(thread);
      }
      else threads_to_update[ident] = new Thread(thread);
    });
  }

  killRecursively() {
    this.health = "Dead";
    Object.keys(this.children).forEach(ident => {
      this.children[ident].killRecursively();
    });
  }
}
