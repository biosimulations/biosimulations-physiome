/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is "Andre's Reference Description Framework".
 *
 * The Initial Developer of the Original Code is
 * David Nickerson <nickerso@users.sourceforge.net>.
 * Portions created by the Initial Developer are Copyright (C) 2007-2008
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */
dojo.provide("andre.ChartData");
dojo.require("dojox.data.CsvStore");
dojo.declare("andre.ChartData", null, {

  /*
    Summary:
      An object to manage the data for a given chart.
  
      Assumes the CSV data file is in the format:
        position,label,x,y
  
      FIXME: should maybe extend dojox.data.CsvStore?
      FIXME: is there a way to tie directly to the HDF5 data file?
  */
  
  // store: dojox.data.CsvStore
  //  The data store containing all the chart data
  store: null,
  
  fetchInProgress: 0,
  fetchedData: null,
  
  constructor: function (/*String*/url) {
    // summary: initialise the data object, creating the CsvStore from the given url.
    if (url && url.length > 0) {
      console.log("Creating ChartData with the URL: " + url);
      this.store = new dojox.data.CsvStore({url: url, label: "label"});
      if (this.store == null) {
        console.log("ERROR: error creating CSV data store");
        return false;
      }
    } else {
      console.log("ERROR: invalid URL provided for the CSV file (" + url + ")");
      return false;
    }
  },
  
  fetchDataByPosition: function (/*String|Number*/position, /*String*/onItemTopic) {
    // summary: 
    console.log("Fetching data for position: " + position);
    this.fetch({'position': position},onItemTopic,position);
  },
  
  fetchDataByLabel: function (/*String*/label, /*String*/onItemTopic) {
    // summary: 
    console.log("Fetching data for label: " + label);
    return this.fetch({'label': label},onItemTopic,label);
  },
  
  fetch: function (/*Object*/query, /*String*/onItemTopic, /*String*/series) {
    // summary: initiate a fetch.
    //console.log("Fetching data for query: " + dojo.toJson(query));
    if (!this.store) {
      console.log("ERROR: missing data store in fetchDataByPosition()");
      return false;
    }
    //console.log("fetch - staring fetch with query: " + dojo.toJson(query));
    this.store.fetch({
      scope: this,
      query: query,
      onItem: function (item, request) {
        //console.log("fetch - item found");
        //var x = this.store.getValue(item,"x",/*default value*/0.0);
        //var y = this.store.getValue(item,"y",/*default value*/0.0);
        //console.log("found the data point: {" + x + "," + y + "}");
        var message = {};
        message.series = series;
        message.request = request; /* in case we need to abort? */
        message.complete = false;
        message.error = false;
        message.x = this.store.getValue(item,"x",/*default value*/0.0);
        message.y = this.store.getValue(item,"y",/*default value*/0.0);
        dojo.publish(onItemTopic,[message]);
      },
      onComplete: function (items, request) {
        //console.log("fetch - fetch complete");
        var message = {};
        message.series = series;
        message.request = request; /* in case we need to abort? */
        message.complete = true;
        message.error = false;
        dojo.publish(onItemTopic,[message]);
      },
      onError: function (error, request) {
        //console.log("fetch - fetch error: " + error);
        var message = {};
        message.series = series;
        message.request = request; /* in case we need to abort? */
        message.complete = false;
        message.error = true;
        message.errorMessage = error;
        dojo.publish(onItemTopic,[message]);
      },
    });
    return true;
  },
  
});