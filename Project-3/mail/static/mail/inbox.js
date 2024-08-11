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

  // Submit compose
  // document.querySelector("#compose-form").addEventListener("submit", send_mail);
  document.querySelector("#compose-form").addEventListener("submit", send_mail);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-details").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  const emails_view = document.querySelector("#emails-view");
  emails_view.style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-details").style.display = "none";

  emails_view.dataset.type = mailbox;

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  show_mails(mailbox, emails_view);
}

async function send_mail(e) {
  e.preventDefault();

  const data = {
    recipients: document.querySelector("#compose-recipients").value,
    subject: document.querySelector("#compose-subject").value,
    body: document.querySelector("#compose-body").value,
  };

  await handle_data("post", "/emails", data);
  load_mailbox("sent");
}

async function handle_data(method, route, data = null) {
  try {
    let res;
    if (method.toLowerCase() === "get") {
      res = await fetch(route);
    } else {
      res = await fetch(route, {
        method: method.toUpperCase(),
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });
    }

    let result;
    try {
      const text = await res.text();
      result = text ? JSON.parse(text) : {};
    } catch (error) {
      console.error("Error parsing JSON:", error);
      result = {};
    }

    if (!res.ok) {
      console.error("Error:", result.error);
      return null;
    } else {
      return result;
    }
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}

async function show_mails(mailbox, emails_view) {
  const emails = await handle_data("get", `/emails/${mailbox}`);

  emails.forEach((email) => {
    const emailDiv = document.createElement("div");
    emailDiv.className = "list-group-item mb-2 rounded border border-secondary";
    emailDiv.style.backgroundColor = email.read ? "#EEEEEE" : "white";

    const content = `
      <h6 id="sender">
        Sender: ${email.sender}
      </h6>
      <h5 id="subject">Subject: ${email.subject}</h5>
      <p>${email.timestamp}</p>
    `;

    emailDiv.innerHTML = content;
    emails_view.appendChild(emailDiv);

    emailDiv.addEventListener("click", () => show_email_details(email.id));
  });
}

async function show_email_details(id) {
  const email_data = await handle_data("get", `/emails/${id}`);
  await handle_data("put", `/emails/${id}`, { read: true });

  const email_details = document.querySelector("#email-details");

  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  email_details.style.display = "block";

  const {
    sender: from,
    recipients: to,
    subject,
    body: content,
    timestamp,
    archived,
  } = email_data;
  const array_header = [{ from }, { to }, { subject }, { timestamp }];

  const header = document.createElement("div");

  array_header.forEach((ele) => {
    const container = document.createElement("div");
    container.className = "d-flex align-items-center mb-2";
    container.innerHTML = `
      ${
        Object.keys(ele)[0].toLowerCase() !== "timestamp"
          ? `<h6 class="mr-2 text-capitalize" style="margin: 0;">${Object.keys(
              ele
            )}:</h6>`
          : ""
      }
      <p style="margin: 0;">${Object.values(ele)}</p>
    `;
    header.appendChild(container);
  });

  const body = document.createElement("div");
  body.innerHTML = content;

  const hr = document.createElement("hr");

  const archiveButton = document.createElement("button");
  archiveButton.className = "btn btn-sm btn-outline-secondary mt-2";
  archiveButton.textContent = archived ? "Unarchive" : "Archive";
  archiveButton.addEventListener("click", () => handle_archive(id, archived));

  const reply = document.createElement("button");
  reply.textContent = "Reply";
  reply.className = "btn btn-sm btn-outline-primary";
  header.appendChild(reply);

  reply.addEventListener("click", () => handle_reply(email_data));

  email_details.innerHTML = "";
  email_details.append(header, archiveButton, hr, body);
}

async function handle_archive(id, archived) {
  await handle_data("put", `/emails/${id}`, { archived: !archived });
  load_mailbox("inbox");
}

function handle_reply(data) {
  compose_email();

  let subject = data.subject;
  if (subject.split(" ")[0].toLowerCase() !== "re:") {
    subject = `Re: ${subject}`;
  }

  document.querySelector("#compose-recipients").value = data.sender;
  document.querySelector("#compose-subject").value = subject;
  document.querySelector(
    "#compose-body"
  ).value = `On ${data.timestamp} ${data.sender} wrote: ${data.body}`;
}
