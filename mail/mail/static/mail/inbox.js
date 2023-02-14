document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);
  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views

  document.querySelector("#body_email")?.remove();
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#body_email")?.remove();

  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  get_emails(mailbox);

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
}

const send_email = (event) => {
  event.preventDefault();

  const recipients = document.querySelector("#compose-recipients");
  const subject = document.querySelector("#compose-subject");
  const body = document.querySelector("#compose-body");

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients.value,
      subject: subject.value,
      body: body.value,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((result) => {
      console.log(result);
      if (result.error) throw Error(result.error);

      alert(result.message);
      load_mailbox("sent");
    })
    .catch((err) => alert(err));

  recipients.value = "";
  subject.value = "";
  body.value = "";
};

const get_email = async (event) => {
  const email = await fetch(`/emails/${event.target.value}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((email) => {
      fetch(`/emails/${event.target.value}`, {
        method: "PUT",
        body: JSON.stringify({
          read: true,
        }),
      });

      return email;
    });

  document.querySelector("#emails-view").style.display = "none";

  const body_email = document.createElement("div");
  const sender = document.createElement("p");
  const recipients = document.createElement("p");
  const subject = document.createElement("p");
  const timestamp = document.createElement("p");
  const body = document.createElement("p");
  const reply_button = document.createElement("button");

  body_email.id = "body_email";
  body.className = "body_email";
  reply_button.className = "btn btn-sm btn-outline-primary";

  sender.innerHTML = `<b>From:</b> ${email.sender}`;
  recipients.innerHTML = `<b>To:</b> ${email.recipients.map((e) => e + " ")}`;
  subject.innerHTML = `<b>Subject:</b> ${email.subject}`;
  timestamp.innerHTML = `<b>Timesstamp:</b> ${email.timestamp}`;
  reply_button.innerHTML = "Reply";

  body.innerHTML = email.body;

  body_email.appendChild(sender);
  body_email.appendChild(recipients);
  body_email.appendChild(subject);
  body_email.appendChild(timestamp);
  body_email.appendChild(reply_button);
  body_email.appendChild(document.createElement("hr"));
  body_email.appendChild(body);

  document.querySelector(".container").appendChild(body_email);

  reply_button.addEventListener("click", () => {
    replyEmail(email);
  });
};

const get_emails = async (mailbox) => {
  const emails = await fetch(`/emails/${mailbox}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((emails) => emails);

  const unordered_list = document.createElement("ul");
  unordered_list.className = "container_emails";

  emails.forEach((email) => {
    const item_list = document.createElement("li");
    const archive = document.createElement("button");
    const timestamp = document.createElement("span");

    timestamp.innerHTML = email.timestamp;
    item_list.innerHTML = email.sender;
    item_list.innerHTML += " Subject: " + email.subject;
    item_list.value = email.id;
    item_list.appendChild(timestamp);
    if (mailbox !== "sent") {
      if (!email.read) {
        item_list.className = "noRead";
      }
      archive.innerHTML = email.archived ? "Desarchivar" : "Archivar";
      archive.value = email.id;
      archive.dataset.archived = email.archived;
      item_list.appendChild(archive);
    }

    archive.addEventListener("click", archive_email);
    item_list.addEventListener("click", get_email);
    unordered_list.appendChild(item_list);
  });
  document.querySelector("#emails-view").appendChild(unordered_list);
};

const archive_email = (event) => {
  const boolean = event.target.innerHTML === "Archivar" ? true : false;

  fetch(`/emails/${event.target.value}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: boolean,
    }),
  });
  window.location.reload();
};

const replyEmail = (email) => {
  console.log(email);
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#body_email").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#compose-recipients").value = email.sender;
  document.querySelector("#compose-subject").value = email.subject.includes(
    "Re:"
  )
    ? email.subject
    : `Re: ${email.subject}`;
  const compose = document.querySelector("#compose-body");

  const verify = email.body.includes("On");
  if (verify) {
    const history = email.body.split("\n").filter((e) => e !== "");
    history.forEach((oldMail) => {
      if (oldMail.includes("On")) {
        compose.value += `${oldMail}\n`;
      } else {
        compose.value += `On ${email.timestamp} ${email.sender} wrote: ${email.body}. `;
      }
    });
    console.log(compose.value);
  } else {
    compose.value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}. `;
  }
};
