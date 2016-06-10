<?php
include_once "config.inc.php";

if (!isset($_GET['id']) || empty($_GET['id']) || !preg_match("/^[A-z0-9]{{$ID_SIZE}}$/", $_GET['id'])) error();
$id = $_GET['id'];

$conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS);
if ($conn === FALSE) error(500, "Database error 1");
if ($conn->select_db($DB_NAME) !== TRUE) error(500, "Database error 2");

$stmt = $conn->prepare("SELECT enabled, url FROM ${DB_PREFIX}urls WHERE id LIKE ? LIMIT 1");
if ($stmt === FALSE) error(500, "Database error 3");
if ($stmt->bind_result($enabled, $url) === FALSE) error(500, "Database error 4");
if ($stmt->bind_param('s', $id) === FALSE) error(500, "Database error 5");
if ($stmt->execute() !== TRUE) error(500, "Database error 6");
$tmp = $stmt->fetch();
if ($tmp === FALSE) error(500, "Database error 7");
else if ($tmp === NULL) error(404, "Link not found");
if ($enabled !== 1) error(410, "Link disabled");
$stmt->close();

// plugin
if (isset($_GET['plugin']) && !empty($_GET['plugin']))
{
    // some anti-nastiness
    if (preg_match("/^[A-z0-9-_]+$/", $_GET['plugin']) === FALSE || !is_file("plugins/$_GET[plugin].php"))
    {
        error();
    }
    /** @noinspection PhpIncludeInspection */
    include "plugins/$_GET[plugin].php";
}
// plain old redirect
else
{
    header("Location: $url");
}

$conn->close();