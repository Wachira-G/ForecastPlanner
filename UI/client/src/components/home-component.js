import React from 'react';
const Home = () => {
  return (
    <div>
    <section className="bg-light text-dark p-5 p-lg-0 pt-lg-5 text-center text-sm-start">
      <div className="container">
        <div className="d-sm-flex align-items-center justify-content-between">
          <div>
            <h2>Are you planning a trip?</h2>
            <p className="lead my-4">
              We organise your trip and make sure everything goes according to plan.
              You can check the weather conditions on your trip dates and schedule your activities!
            </p>
          </div>
          <img className="img-fluid w-50 d-none d-sm-block" src="assets/trvelsmany.jpeg" alt="Plan your trip" style={{ maxWidth: "35%" }} />
        </div>
      </div>
    </section>
    <section className="p-5" id="weather">
         <div className="container weather-container">
           <div className="weather-input">
             <h4>Enter Name Of A City</h4>
             <input className="city-input" type="text" placeholder="E.g., Nairobi, Kisumu" />
             <button className="search-btn bg-warning">Search</button>
             <div className="separator"></div>
             <button className="location-btn">Use Current Location</button>
           </div>
           <div className="weather-data">
             <div className="current-weather">
               <div className="details">
                 <h2>_______ ( ______ )</h2>
                 <h6>Temperature: __°C</h6>
                 <h6>Wind: __ M/S</h6>
                 <h6>Humidity: __%</h6>
               </div>
             </div>
             <div className="days-forecast">
               <h2>5-Days Forecast</h2>
               <ul className="weather-cards">
                 <li className="card">
                   <h3>( ______ )</h3>
                   <h6>Temp: __°C</h6>
                   <h6>Wind: __ M/S</h6>
                   <h6>Humidity: __%</h6>
                 </li>
                 <li className="card">
                   <h3>( ______ )</h3>
                   <h6>Temp: __°C</h6>
                   <h6>Wind: __ M/S</h6>
                   <h6>Humidity: __%</h6>
                 </li>
                 <li className="card">
                   <h3>( ______ )</h3>
                   <h6>Temp: __°C</h6>
                   <h6>Wind: __ M/S</h6>
                   <h6>Humidity: __%</h6>
                 </li>
                 <li className="card">
                   <h3>( ______ )</h3>
                   <h6>Temp: __°C</h6>
                   <h6>Wind: __ M/S</h6>
                   <h6>Humidity: __%</h6>
                 </li>
                 <li className="card">
                   <h3>( ______ )</h3>
                   <h6>Temp: __°C</h6>
                   <h6>Wind: __ M/S</h6>
                   <h6>Humidity: __%</h6>
                 </li>
               </ul>
             </div>
           </div>
         </div>
       </section>

        <section className="section bg-secondary p-5" id="about">
          <div className="container">
            <h2 className="text-center text-dark">About us</h2>
            <p className="lead text-center text-warning mb-5">
              Learn more about what we do.
            </p>
            <div className="row g-5">
              <div className="col-md">
                <div className="card bg-secondary text-light">
                  <img src="assets/about_us_01.jpg" className="card-img-top img-fluid" alt="..." />
                  <div className="card-body">
                    <h5 className="card-title">Plan on taking a trip!</h5>
                    <p className="card-text">Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum vitae natus qui reprehenderit, beatae nobis!</p>
                    <a href="#" className="card-link text-warning" id="location">Lets Travel!</a>
                  </div>
                </div>
              </div>
              <div className="col-md">
                <div className="card bg-warning text-dark">
                  <img src="assets/about_us2.jpg" className="card-img-top img-fluid" alt="..." />
                  <div className="card-body">
                    <h5 className="card-title">When is the suitable time?</h5>
                    <p className="card-text">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolor quaerat culpa atque ab repudiandae ipsa.</p>
                    <a href="#" className="card-link text-secondary" id="signup">Schedule a trip</a>
                  </div>
                </div>
              </div>
              <div className="col-md">
                <div className="card bg-secondary text-white">
                  <img src="assets/notification.jpg" className="card-img-top img-fluid" alt="..." />
                  <div className="card-body">
                    <h5 className="card-title">Stay up to date</h5>
                    <p className="card-text">Lorem ipsum dolor sit amet consectetur adipisicing elit. Iste ad qui iusto error alias eaque.</p>
                    <a href="#" className="card-link text-warning">Get more access</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="p-5" id="contact">
          <div className="container">
            <div className="row g-4 ms-auto">
              <div className="col-md-6">
                <h2 className="text-center mb-4" id="faq">Frequently Asked Questions</h2>
                <div className="accordion accordion-flush" id="question">
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                        Is this a weather forecasting App?
                      </button>
                    </h2>
                    <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#question">
                      <div className="accordion-body accordion-flush">Lorem ipsum dolor sit amet consectetur adipisicing elit. Odit facilis maiores optio fugit atque! Ab ea consectetur nihil dolorem velit.</div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
                        Do I have to sign in?
                      </button>
                    </h2>
                    <div id="flush-collapseTwo" className="accordion-collapse collapse" data-bs-parent="#question">
                      <div className="accordion-body accordion-flush">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam dignissimos exercitationem eligendi natus vitae!</div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
                        Can you recommend travel destinations?
                      </button>
                    </h2>
                    <div id="flush-collapseThree" className="accordion-collapse collapse" data-bs-parent="#question">
                      <div className="accordion-body accordion-flush">Lorem ipsum dolor sit amet consectetur adipisicing elit. Dignissimos quam dolor architecto quae est eveniet consectetur nisi ea a reprehenderit praesentium voluptatibus ex cum, consequuntur non doloribus deleniti velit? Placeat.</div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFive" aria-expanded="false" aria-controls="flush-collapseFive">
                        How can I contact customer support?
                      </button>
                    </h2>
                    <div id="flush-collapseFive" className="accordion-collapse collapse" data-bs-parent="#question">
                      <div className="accordion-body accordion-flush">Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit eum, alias itaque illum doloribus nostrum, deserunt voluptatem excepturi, voluptate officiis dolorem. At laboriosam nobis, adipisci libero repudiandae eius nemo laudantium?</div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseSix" aria-expanded="false" aria-controls="flush-collapseSix">
                        How can I update my profile information?
                      </button>
                    </h2>
                    <div id="flush-collapseSix" className="accordion-collapse collapse" data-bs-parent="#question">
                      <div className="accordion-body accordion-flush">Lorem ipsum dolor sit amet consectetur adipisicing elit. Earum odio laborum beatae numquam ipsum dicta maxime corrupti temporibus. Officiis consequatur temporibus culpa, repellat voluptate ullam at dignissimos reprehenderit enim ex.</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form">
                  <h2 className="text-center mb-4">Feedback Form</h2>
                  <form method="POST">
                    <div className="mb-3">
                      <label htmlFor="name" className="visually-hidden" data-placeholder-label="Name (optional)">Name (optional)</label>
                      <input type="text" className="form-control" id="name" placeholder="Name (optional)" />
                    </div>
                    <div className="mb-3">
                      <label htmlFor="email" className="visually-hidden" data-placeholder-label="Email (optional)">Email (optional)</label>
                      <input type="email" className="form-control" id="email" placeholder="Email (optional)" />
                    </div>
                    <div className="mb-3">
                      <label htmlFor="feedback" className="visually-hidden" data-placeholder-label="Feedback">Feedback</label>
                      <textarea className="form-control" id="feedback" rows="5" placeholder="Talk to us ..."></textarea>
                    </div>
                    <button type="submit" className="btn btn-warning">Submit</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="section p-5 bg-secondary" id="reviews">
          <div className="container">
            <h2 className="text-center text-dark">Reviews</h2>
            <p className="lead text-center text-warning mb-5">
              What do our users say about us?
            </p>
            <div className="row g-4">
              <div className="col-md-6 col-lg-3">
                <div className="card bg-light">
                  <div className="card-body text-center">
                    <img src="assets/pic-person-01.jpg" className="card-img-top card-avatar rounded-circle mb-3" alt="avatar" />
                    <h3 className="card-title mb-3">Jane Doe</h3>
                    <p className="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-lg-3">
                <div className="card">
                  <div className="card-body text-center">
                    <img src="assets/pic-person-02.jpg" className="card-img-top card-avatar rounded-circle mb-3" alt="avatar" />
                    <h3 className="card-title mb-3">Ian Smith</h3>
                    <p className="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-lg-3">
                <div className="card bg-light">
                  <div className="card-body text-center">
                    <img src="assets/pic-person-03.jpg" className="card-img-top card-avatar rounded-circle mb-3" alt="avatar" />
                    <h3 className="card-title mb-3">Marie Jones</h3>
                    <p className="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-lg-3">
                <div className="card bg-light">
                  <div className="card-body text-center">
                    <img src="assets/pic-person-02.jpg" className="card-img-top card-avatar rounded-circle mb-3" alt="avatar" />
                    <h3 className="card-title mb-3">Peters Faith</h3>
                    <p className="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        </div>
      );
    };

    export default Home;
