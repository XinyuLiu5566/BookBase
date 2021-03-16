import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";
import Home from './components/Home';
import RankAuthorPage from './components/RankAuthorPage';
import RankBookPage from './components/RankBookPage';
import { Menu } from 'semantic-ui-react'



function App() {

  return (
    <Router>
      <div>
        {/* <nav> */}
        <Menu>
        <Menu.Item header>
          <Link to="/">Home</Link>
        </Menu.Item>
        <Menu.Item header>
          <Link to="/vis/top-authors">Top Authors</Link>
        </Menu.Item>
        <Menu.Item header>
          <Link to="/vis/top-books">Top Books</Link>
        </Menu.Item>
      </Menu>
        {/* </nav> */}

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/vis/top-authors">
            <RankAuthorPage />
          </Route>
          <Route path="/vis/top-books">
            <RankBookPage />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
