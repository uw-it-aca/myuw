import utils from '../mixin/utils'

it('ucfirst', () => {
  expect(utils.methods.ucfirst('test')).toEqual('Test');
  expect(utils.methods.ucfirst('test string')).toEqual('Test string');
});