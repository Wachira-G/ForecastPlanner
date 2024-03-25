import React from 'react';

function HeroSection() {
  return (
    <section className="bg-light text-dark p-5 p-lg-0 pt-lg-5 text-center text-sm-start">
      <div className="container">
        {/* Your hero section content */}
        <div class="container">
            <div class="d-sm-flex align-items-center justify-content-between">
                <div>
                    <h1>Planning a trip?</h1>
                    <p class="lead my-4">
                        Check out the weather conditions at your trip destinations!
                    </p>
                    <div class="d-grid gap-2">
                        <div class="col-auto">
                            <button class="btn btn-warning btn-lg mb-2">Check Forecast</button>
                        </div>
                        <div class="col-auto">
                            <button class="btn btn-warning btn-lg mb-2">Select Trip dates</button>
                        </div>
                        <div class="col-auto">
                            <button class="btn btn-warning btn-lg mb-2">Location</button>
                        </div>
                    </div>
                </div>
                <img class="img-fluid w-50 d-none d-sm-block" src="assets/trvelsmany.jpeg" alt="Plan your trip" style="max-width: 45%;">
            </div>
        </div>
      </div>
    </section>
  );
}
