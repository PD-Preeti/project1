$(document).ready(function() {
  var table = $('#dashboard_report').DataTable({
    responsive: true,
    searching: false,
    "bLengthChange": false,
    dom: 'Bfrtip',
    buttons: [
      {
        extend: 'csvHtml5',
        text: 'Export CSV',
      }
    ],
  })
  .columns.adjust()
  .responsive.recalc();
});

try{
  setTimeout(() => {
    const getFilterSection = document.querySelector('#filterSection'),
        dtButtons = document.querySelector('.dt-buttons');
    getFilterSection.append(dtButtons);

    // Member values
    $('.user_search').chosen();
    document.getElementById('output-user_search').innerHTML = location.search;

  }, 200)
}catch(err){console.error(err)}