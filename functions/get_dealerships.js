/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     console.log("Running get-dealerships:")
     console.log("Cloudant URL: "+ params.COUCH_URL)
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });

     try {
         const fields = ["id","city","state","st","address","zip","lat","long","short_name","full_name"];
         
         const selector = (params.state)? {st: {"$eq": params.state}} : {};
         const query = {selector: selector, fields: fields}
         
         let db = cloudant.db.use('dealerships')
         let dealerships = await db.find(query);
         return dealerships ;
     } catch (error) {
         return { error: error.description };
     }
 
 }