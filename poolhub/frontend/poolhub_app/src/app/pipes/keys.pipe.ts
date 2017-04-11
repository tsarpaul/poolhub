import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'keys',
  pure: false
})
export class KeysPipe implements PipeTransform {

  transform(value: Object, args?: any): Array<any> {
    return Object.keys(value);
  }
}
