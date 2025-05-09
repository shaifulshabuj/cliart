// JavaScript example file

import { Component } from 'react';
import * as utils from './utils';

// A simple class
class ExampleClass extends Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0
    };
  }
  
  incrementCount() {
    this.setState({ count: this.state.count + 1 });
  }
  
  render() {
    return (
      <div>
        <h1>Counter: {this.state.count}</h1>
        <button onClick={() => this.incrementCount()}>Increment</button>
      </div>
    );
  }
}

// A function
function calculateSum(a, b) {
  return a + b;
}

// Arrow function
const multiply = (a, b) => a * b;

// Variable
const API_URL = 'https://api.example.com';

export default ExampleClass;
