<?php
include_once "../config.inc.php";
header("Content-Type: text/plain");

if (isset($_GET['help'])) die(<<<'HELP'
Make a new short URL.

Required data (GET or POST):
    - "api": Your API token
    - "url": The _FULL_ URL to shorten (url encoded!) Must be ASCII [rfc2396](http://www.faqs.org/rfcs/rfc2396.html).

Possible responses:
    - 200 OK: The request was fulfilled
    - 400 Bad Request: Missing input data
    - 403 Forbidden: Your api token is not valid or it has been revoked
    - 404 Not Found: The id does not exist

Example GET request:
    >   GET /api/new?api=aTokenHere&url=https%3A%2F%2Fdries007.net
    <   https://l.dries007.net/0000000000

HELP
);

if (!isset($_REQUEST['api'], $_REQUEST['url'])) error(400, "Missing input data");

$api = $_REQUEST['api'];
$url = $_REQUEST['url'];

if (!preg_match("/^[A-z0-9]{{$ID_SIZE}}$/", $api)) error(400, "Input token invalid");
if (filter_var($url, FILTER_VALIDATE_URL) === FALSE) error(400, "Input url invalid");

if (strlen($url) > $URL_SIZE) error(414, "Url too long");

$conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS);
if ($conn === FALSE) error(500, "Database error 1");
if ($conn->select_db($DB_NAME) !== TRUE) error(500, "Database error 2");

$stmt = $conn->prepare("SELECT id FROM ${DB_PREFIX}tokens WHERE token LIKE ? LIMIT 1");
if ($stmt === FALSE) error(500, "Database error 3");
if ($stmt->bind_result($token_id) === FALSE) error(500, "Database error 4");
if ($stmt->bind_param('s', $api) === FALSE) error(500, "Database error 5");
if ($stmt->execute() !== TRUE) error(500, "Database error 6");
$tmp = $stmt->fetch();
if ($tmp === FALSE) error(500, "Database error 7");
else if ($tmp === NULL) error(403, "Bad API token");
$stmt->close();

do
{
    $id = generateRandomString($ID_SIZE);
    $stmt = $conn->prepare("SELECT 1 FROM ${DB_PREFIX}urls WHERE id LIKE ? LIMIT 1");
    if ($stmt === FALSE) error(500, "Database error 8");
    if ($stmt->bind_result($exists) === FALSE) error(500, "Database error 9a");
    if ($stmt->bind_param('s', $id) === FALSE) error(500, "Database error 9b");
    if ($stmt->execute() !== TRUE) error(500, "Database error 10");
    $tmp = $stmt->fetch();
    if ($tmp === FALSE) error(500, "Database error 11");
}
while ($tmp === TRUE);

$stmt->close();

$stmt = $conn->prepare("INSERT INTO ${DB_PREFIX}urls (id, url, token) VALUES (?, ?, ?)");
if ($stmt === FALSE) error(500, "Database error 12");
if ($stmt->bind_param('ssi', $id, $url, $token_id) === FALSE) error(500, "Database error 13");
if ($stmt->execute() !== TRUE) error(500, "Database error 14");
if ($stmt->affected_rows == 0) error(410, "");
$stmt->close();

echo "$LINK_PREFIX$id";


