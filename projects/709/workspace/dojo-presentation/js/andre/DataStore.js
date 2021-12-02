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
/* define a new data store which extends the actual data store to be used
  - the data store uses URI's as internal identities, but we want to return XHTML
    valid ID's with the getIdentity() method (can still use
    store.getValue(item,'uri') to retrieve the actual URI).
  - For compatibility, want the final ID to match: [A-Za-z][A-Za-z0-9:_.-]*
  - this may not always be a JSON based ItemFileReadStore so code shouldn't make
    any assumptions about it (i.e., use store.getValue(item,attribute) rather 
    than item.attribute
 */
dojo.provide("andre.DataStore");
dojo.require("dojo.data.ItemFileReadStore");
dojo.declare("andre.DataStore",dojo.data.ItemFileReadStore, {
  getIdentity: function(item) {
    // get the original ID from the underlying data store
    var id = this.inherited(arguments);
    // FIXME: no longer using URI's for ID's so this is not needed.
    //console.log("returning ID: " + id);
    return id;
    /*
    // check if it already mapped
    if (this.uriMap[id]) {
      // do nothing
    } else {
      // create a new XHTML id for this URI
      this.uriMap[id] = "a_" + this.counter;
      this.counter++;
    }
    //console.debug("uriMap: " + this.uriMap[id]);
    return this.uriMap[id];
    */
  },
  /*uriMap: {},
  counter: 0*/
});
