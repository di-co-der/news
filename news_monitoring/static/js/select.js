$(document).ready(function() {
      $('#companies').select2({
          placeholder: "Search companies",
          ajax: {
              url: companySearch,
              dataType: "json",
              delay: 250,
              data: function(params) {
                  return { q: params.term };
              },
              processResults: function(data) {
                  return {
                      results: $.map(data, function(company) {
                          return { id: company.id, text: company.name };
                      })
                  };
              },
              cache: true
          },
          minimumInputLength: 2, // Start searching after 2 characters
          allowClear: true
      });
});
