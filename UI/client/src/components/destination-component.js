import React, { Component } from "react";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import { isEmail } from "validator";

import { connect } from "react-redux";
import { destination } from "../actions/post-profile";

const required = (value) => {
  if (!value) {
    return (
      <div className="alert alert-danger" role="alert">
        This field is required!
      </div>
    );
  }
};

class Destination extends Component {
  constructor(props) {
    super(props);
    this.handlePostDestination = this.handlePostDestination.bind(this);
    this.onChangeLocation = this.onChangeLocation.bind(this);
    this.onChangeDate = this.onChangeDate.bind(this);
    this.onChangeDays = this.onChangeDays.bind(this);

    this.state = {
      location_name: "",
      date: "",
      days: "",
      successful: false,
    };
  }

  onChangeLocation(e) {
    this.setState({
      location_name: e.target.value,
    });
  }

  onChangeDate(e) {
    this.setState({
      date: e.target.value,
    });
  }

  onChangeDays(e) {
    this.setState({
      days: e.target.value,
    });
  }

  handlePostDestination(e) {
    e.preventDefault();

    this.setState({
      successful: false,
    });

    this.form.validateAll();

    if (this.checkBtn.context._errors.length === 0) {
      this.props
        .dispatch(
          destination(
            this.state.location_name,
            this.state.date,
            this.state.days)
        )
        .then(() => {
          this.setState({
            successful: true,
          });
        })
        .catch(() => {
          this.setState({
            successful: false,
          });
        });
    }
  }

  render() {
    const { message } = this.props;

    return (
      <div className="col-md-12">
        <div className="card card-container">

          <Form
            onSubmit={this.handlePostDestination}
            ref={(c) => {
              this.form = c;
            }}
          >
            {!this.state.successful && (
              <div>
              <div className="mb-3">
                <label htmlFor="cityname">City Name:</label>
                <Input
                  type="text"
                  name="location_name"
                  className="form-control"
                  id="name"
                  placeholder="Nairobi"
                  onChange={this.handleChange}
                  validations={[required]}
                />
              </div>

              <div className="mb-3">
                <label htmlFor="travelDate">Travel Dates:</label>
                <Input
                  type="date"
                  name="date"
                  className="form-control"
                  id="travelDate"
                  placeholder="12/12/2020"
                  onChange={this.handleChange}
                  validations={[required]}
                />
              </div>

              <div className="mb-3">
                <label htmlFor="activities">Number of days:</label>
                <Input
                  type="number"
                  name="days"
                  className="form-control"
                  id="activities"
                  placeholder="2"
                  onChange={this.handleChange}
                  validations={[required]}
                />
              </div>

                <div className="form-group">
                  <button className="btn btn-warning btn-block">Enter</button>
                </div>
              </div>
            )}

            {message && (
              <div className="form-group">
                <div className={ this.state.successful ? "alert alert-success" : "alert alert-danger" } role="alert">
                  {message}
                </div>
              </div>
            )}
            <CheckButton
              style={{ display: "none" }}
              ref={(c) => {
                this.checkBtn = c;
              }}
            />
          </Form>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { message } = state.message;
  return {
    message,
  };
}

export default connect(mapStateToProps)(Destination);
