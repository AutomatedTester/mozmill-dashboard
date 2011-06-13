function elastic_search(context,query){
   elastic ="http://10.250.1.199:9200/release/release/_search"
   context.first_result=query.from
   context.last_result=parseInt(query.from)+parseInt(query.size)
   
   $.ajax({
     url:elastic,
     type:"POST",
     dataType: "json",
     data: JSON.stringify(query),
     success: function(data){
       context.total_results=data.hits.total
       var hits = data.hits.hits

       context.reports = []
       for (x in hits){
           context.reports.push({
               'ID' : hits[x]._id,
               'Date' : hits[x]._source.time_end,
               'index' : x
           })
       }
       context
         .render('results.mustache')
         .replace('#main');
     }
   });


}

(function($) {
  var app = $.sammy(function() {
      this.use(Sammy.Mustache)
  //var context = this

      this.get('#/', function() {
        $('#main').text('');
      });

      this.get('#/hello/:name', function() {
        // set local vars
        this.title = 'Hello!'
        this.name = this.params.name;
        // render the template and pass it through mustache
        this
          .render('mytemplate.mustache')
          .replace('#main');
      });


      this.get('#/search/:from', function() {
        query = {
           "from":this.params.from,
           "size":50,
           "sort":[{"time_end":"desc"},"_score"],
           "query":{ 
               "term":{ 
                   "application_name":"firefox" 
               }
           }
        }
        elastic_search(this,query)
      })
 
    
      this.get('#/comment/:id', function(){
        this.id=this.params.id
        this 
          .render('comment.mustache')
          .replace('#main');

      })
      this.post('#/comment/',function(){
       //TODO: this is obviously really insecure. The user should not have plain write access to the comments db
       var context=this
       comment_doc={
         'report':this.params.id,
         'name':this.params.commenter,
         'comment':this.params.comment
       }
       var elastic = 'http://10.250.1.199:8000/'


       $.post(elastic,comment_doc,function(){
         context.redirect('#','/report/'+context.params.id)
       });
       context.redirect('#','/report/'+context.params.id)
       console.debug(comment_doc) 
       console.debug(this)
      });

      this.get('#/owen/',function(){
       //TODO: this is obviously really insecure. The user should not have plain write access to the comments db
       comment_doc={
         'report':'7da43dc703ad47e7276132c0990fcd24',
         'name':'Owen',
         'comment':'What is the meaning of a comment?'
       }
       console.debug(comment_doc)
       /*comment_doc={
         'report':this.params.id,
         'name':this.params.commenter,
         'comment':this.params.comment
       }*/
       var elastic = 'http://10.250.1.199:8000/'


       $.post(elastic,comment_doc,function(){
          console.debug('yipee');
       });
 
       console.debug(comment_doc) 
       console.debug(this)
      })

          

      this.get('#/report/:id', function() {
        elastic_get = 'http://10.250.1.199:9200/release/release/'
        var context = this
        $.get(elastic_get+this.params.id,function(data){
          hit = data._source
           
          context.id = hit._id
          context.app_name = hit.application_name
          context.platform_version = hit.application_version
          context.app_locale = hit.application_locale
          context.platform_buildID = hit.platform_buildid
          context.app_sourcestamp = hit.platform_repository+'/rev/'+hit.platform_changeset
          context.system=hit.system_info.system
          context.system_version = hit.system_info.version
          context.service_pack = hit.system_info.service_pack
          context.cpu = hit.system_info.processor
          context.time_start = hit.time_start
          context.time_end = hit.time_end
          context.passed = hit.tests_passed
          context.failed = hit.tests_failed
          context.skipped = hit.tests_skipped

          context.results=[]
          for (x in hit.results){
            result = {
              "status":"TODO: figure how status is determined",
              "filename":hit.results[x].filename,
              "test":hit.results[x].name
            }
            context.results.push(result)
          }
          $.get('http://10.250.1.199:9200/foocomments/foocomments/_search?q=report:'+context.params.id,function(data){
            context.comments = []
            var comment_hits=data.hits.hits
            for (x in comment_hits){
              comment = {
                "name":comment_hits[x]._source.name,
                "comment":comment_hits[x]._source.comment,
              }
              context.comments.push(comment)
            }
          },'json')
          context 
          .render('single_report.mustache')
          .replace('#main');

          console.debug(data)
        },'json')
      });

      this.get('#/:test', function() {
        $('#main').text(this.params.test);
      });
  });

  $(function() {
    app.run()
  });
})(jQuery);
