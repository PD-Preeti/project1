// Link Active check
const routeChange = () => {
  const path = location.pathname;
  const linkObj = new Map([
    ["/adminboard/adminhome/", "home"],
    ["/adminboard/createcourse/", "createcourse"],
    ["/adminboard/assign/", "assigncourse"],
    ["/adminboard/addmodule/", "addmodule"],
    ["/adminboard/casestudy/", "casestudy"],
    ["/adminboard/viewmodule/", "viewmodule"],
    ["/adminboard/finalquest/", "finalquest"],
    ["/adminboard/people/", "people"],
    ["/adminboard/submission/", "submission"],
    ["/adminboard/userassessment/", "userassessment"],
    ["/adminboard/questions/", "questions"],
    ["/adminboard/configuration/", "configuration"],
  ]);

  for (let [key, value] of linkObj) {
    if (path === key) {
      let link = document.querySelector(`[data-id = "${value}"]`);
      link.classList.add("uk-active");
    }
  }
};

routeChange();
