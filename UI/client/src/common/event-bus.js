/**
 * Module: eventBus
 * Description: Implements a simple event bus pattern using the browser's document object.
 *              Provides methods for subscribing to events, dispatching events with data, and removing event listeners.
 */
const eventBus = {
  /**
   * Method: on
   * Description: Subscribes to a specified event and invokes the provided callback function when the event is triggered.
   * @param {string} event - The name of the event to subscribe to
   * @param {Function} callback - The callback function to be executed when the event is triggered
   */
  on(event, callback) {
    document.addEventListener(event, (e) => callback(e.detail));
  },

  /**
   * Method: dispatch
   * Description: Dispatches a custom event with the specified name and data attached.
   * @param {string} event - The name of the event to dispatch
   * @param {any} data - The data to be passed along with the event
   */
  dispatch(event, data) {
    document.dispatchEvent(new CustomEvent(event, { detail: data }));
  },

  /**
   * Method: remove
   * Description: Removes the specified event listener.
   * @param {string} event - The name of the event whose listener needs to be removed
   * @param {Function} callback - The callback function to be removed from the event listener
   */
  remove(event, callback) {
    document.removeEventListener(event, callback);
  },
};

// Export the eventBus object
export default eventBus;
