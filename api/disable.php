<?php
include_once "../config.inc.php";
header("Content-Type: text/plain");

if (isset($_GET['help'])) die(<<<'HELP'
Disable a short URL you made.

Warning: This action is irreversible.

Required data (GET or POST):
    - "api": Your API token
    - "id": The ID to disable

Possible responses:
    - 200 OK: the request was fulfilled
    - 400 Bad Request: Missing input data
    - 403 Forbidden: Your api token is not the owner of the id
    - 404 Not Found: The id does not exist
    - 410 Gone: The id has already been disabled

Example GET request:
    >   GET /api/disable?api=aTokenHere&id=0000000000
    <   OK

HELP
);

if (!isset($_REQUEST['api'], $_REQUEST['id'])) error(400, "Missing input data");

$id = $_REQUEST['id'];
$api = $_REQUEST['api'];

if (!preg_match("/^[A-z0-9]{{$ID_SIZE}}$/", $id)) error(400, "Input id invalid");
if (!preg_match("/^[A-z0-9]{{$ID_SIZE}}$/", $api)) error(400, "Input token invalid");

$conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS);
if ($conn === FALSE) error(500, "Database error 1");
if ($conn->select_db($DB_NAME) !== TRUE) error(500, "Database error 2");

$stmt = $conn->prepare("SELECT enabled, ${DB_PREFIX}tokens.token FROM ${DB_PREFIX}urls LEFT JOIN ${DB_PREFIX}tokens ON ${DB_PREFIX}urls.token=${DB_PREFIX}tokens.id WHERE ${DB_PREFIX}urls.id LIKE ? LIMIT 1");
if ($stmt === FALSE) error(500, "Database error 3");
if ($stmt->bind_result($enabled, $owner) === FALSE) error(500, "Database error 4");
if ($stmt->bind_param('s', $id) === FALSE) error(500, "Database error 5");
if ($stmt->execute() !== TRUE) error(500, "Database error 6");
$tmp = $stmt->fetch();
if ($tmp === FALSE) error(500, "Database error 7");
else if ($tmp === NULL) error(404, "Link not found");

if ($owner !== $api) error(403, "Not owner");
$stmt->close();

$stmt = $conn->prepare("UPDATE ${DB_PREFIX}urls SET enabled=FALSE WHERE enabled=TRUE AND token=? AND id=? LIMIT 1");
if ($stmt === FALSE) error(500, "Database error 8");
if ($stmt->bind_param('is', $token_id, $id) === FALSE) error(500, "Database error 9");
if ($stmt->execute() !== TRUE) error(500, "Database error 10");
if ($stmt->affected_rows == 0) error(410, "Already disabled");
$stmt->close();

echo "OK";