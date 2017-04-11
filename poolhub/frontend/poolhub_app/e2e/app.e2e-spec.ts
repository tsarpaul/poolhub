import { PoolhubAppPage } from './app.po';

describe('poolhub_app App', () => {
  let page: PoolhubAppPage;

  beforeEach(() => {
    page = new PoolhubAppPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
