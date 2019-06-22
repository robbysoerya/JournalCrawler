import React from "react";
import $ from 'jquery'
class Home extends React.Component {
  constructor(props) {
      super(props)
      this.state = {
          url: '',
          limit: '',
          crawlingStatus: null,
          data: null,
          taskID: null,
          uniqueID: null
      }
      this.statusInterval = 1
  }

    handleChange = event => {
        this.setState({
            [event.target.id]: event.target.value
        });
    }

  handleStartButton = (event) => {
    if (!this.state.url) return false;

    // send a post request to client when form button clicked
    // django response back with task_id and unique_id.
    // We have created them in views.py file, remember?
    $.post('/api/crawl/', { url: this.state.url, limit: this.state.limit }, resp => {
        if (resp.error) {
            alert(resp.error)
            return
        }
        // Update the state with new task and unique id
        this.setState({
            taskID: resp.task_id,
            uniqueID: resp.unique_id,
            crawlingStatus: resp.status
        }, () => {
            // ####################### HERE ########################
            // After updating state, 
            // i start to execute checkCrawlStatus method for every 2 seconds
            // Check method's body for more details
            // ####################### HERE ########################
            this.statusInterval = setInterval(this.checkCrawlStatus, 2000)
        });
    });
  }

  componentWillUnmount() {
      // i create this.statusInterval inside constructor method
      // So clear it anyway on page reloads or 
      clearInterval(this.statusInterval)
      }
  
  
  dismissAlert() {
    this.setState({'error': false});  
  }

    renderError(){
    return (
      <div className="col-xs-12">
          <div className="alert alert-danger alert-dismissible" role="alert">
              <button type="button" className="close" onClick={this.dismissAlert}
              aria-label="Close">
                  <span aria-hidden="true">&times;</span>
              </button>
              { this.state.error }
          </div>
      </div>      
    );
  }

    renderData() {
        return (
            <div>
                <table className="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>No.</th>
                            <th>Url</th>
                            <th>Title</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.data.map(function (data,i){
                            return(
                            <tr key={i+1}>
                                <td>{i+1}</td>
                                <td>{data['url']}</td>
                                <td>{data['title']}</td>
                            </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        );
    }



    renderButton() {
    return (
        <button type="submit" onClick={this.handleStartButton} className="btn btn-primary btn-sm">
        Run Crawl
        </button>
        
    );
    }

    renderCheck() {
    return (
        <button type="submit" onClick={this.checkCrawlStatus} className="btn btn-primary btn-sm">
        Check
        </button>
        
    );
}

    renderText() {
        return (
            <div>
            <div>Your Task ID : {this.state.taskID}</div>
            <div>Your Unique ID : {this.state.uniqueID}</div>
            <div>Status Crawl : {this.state.crawlingStatus}</div>
            </div>
        );
    }

  checkCrawlStatus = () => {
      // this method do only one thing.
      // Making a request to server to ask status of crawling job
      $.get('/api/crawl/',
            { task_id: this.state.taskID, unique_id: this.state.uniqueID }, resp => {
          if (resp.data) {
              // If response contains a data array
              // That means crawling completed and we have results here
              // No need to make more requests.
              // Just clear interval
              //clearInterval(this.statusInterval)
              this.setState({
                  data: resp.data,
                  exist: true 
              })
          } else if (resp.error) {
              // If there is an error
              // also no need to keep requesting
              // just show it to user
              // and clear interval
              //clearInterval(this.statusInterval)
            //  alert(resp.error)
          } else if (resp.status) {
              // but response contains a `status` key and no data or error
              // that means crawling process is still active and running (or pending)
              // don't clear the interval.
              this.setState({
                  crawlingStatus: resp.status
              });
          }
      })
  }
  
  render () {
    // render componenet
      return (<div>
          <h1 className="page-title">Journal Scan Crawler</h1>
          <hr />
          <div className="container">
              <div className="row">
                        <div className="input-group mb-3">
                            <div className="input-group-prepend">
                                <span className="input-group-text" id="basic-addon3">URL</span>
                            </div>
                            <input type="text" onChange={this.handleChange} className="form-control" id="url" aria-describedby="basic-addon3"/>
                        </div>
                      <input placeholder="Limit" className="form-control col-md-1" type="number" pattern="[0-9]" onChange={this.handleChange} id="limit" aria-describedby="basic-addon3"></input>
                      <button type="submit" onClick={this.handleStartButton} className="btn btn-primary mx-sm-3">Run Crawl</button>
                  </div>
              </div>
          <hr />
          <div>{this.state.taskID ? this.renderText() : null}</div>
          <div></div>{this.state.exist ? this.renderData() : null}</div>
          
    )
  }
}

export default Home