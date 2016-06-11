<?php

$LINK_PREFIX = null; // "https://example.com/" <- include the trailing slash!
$ID_SIZE = 10;
$URL_SIZE = 2048;
$DB_USER = "links";
$DB_NAME = "links";
$DB_PASS = null; // "some secure password here"
$DB_HOST = "localhost";
$DB_PREFIX = "links_"; // can be empty, but not null!
$SHOW_PLUGINS = TRUE;

// Don't forget to set to false in production!
$DEBUG = FALSE;

// -------------------- Some helper functions --------------------

if ($DEBUG)
{
    error_reporting(E_ALL);
    ini_set("display_errors", 1);
}

function error($code = 400, $message = "Bad Request")
{
    header("Content-Type: text/plain");
    http_response_code($code);
    die($message);
}

/**
 * @param int $length
 * @return string
 *
 * Makes a random string of size $length, with at least 1 numer, lower and uppercase character.
 * Not cryptographically secure!
 */
function generateRandomString($length = 10)
{
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    do {
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
    }
    while (!preg_match('/^\S*(?=\S{8,})(?=\S*[a-z])(?=\S*[A-Z])(?=\S*[\d])\S*$/', $randomString));
    /* Thanks password complexity regex: http://stackoverflow.com/a/8141210
     * I use this to make sure the random string contains at least some complexity.
     * ^            : anchored to beginning of string
     * \S*          : any set of characters
     * (?=\S{8,})   : of at least length 8
     * (?=\S*[a-z]) : containing at least one lowercase letter
     * (?=\S*[A-Z]) : and at least one uppercase letter
     * (?=\S*[\d])  : and at least one number
     * $            : anchored to the end of the string
     */
    return $randomString;
}