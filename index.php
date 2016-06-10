<?php include_once "config.inc.php" ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!--
        Copyright (C) 2016 Dries K. aka Dries007
        Build with Bootstrap v4
    -->
    <meta name="description" content="Dries007's Private URL-shortener.">
    <meta name="author" content="Dries007">

    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="/css/custom.css" rel="stylesheet">
    <title>Dries007's Private URL-shortener</title>
</head>
<body>

<div class="container">
    <h1 class="m-t-1">Dries007's Private URL-shortener</h1>
    <p class="lead">This is (probably) not the page you are looking for!</p>
    <?php if ($DEBUG) echo '<div class="alert alert-danger" role="alert"><strong>Danger!</strong> Debug is enabled</div>'?>
    <p>If you see this page, there is a good chance something has gone wrong. Try your link again!<br>
        It should have this format: <code><?php echo $LINK_PREFIX; for ($i = 0; $i < $ID_SIZE; $i++) echo $i % 10; ?></code></p>
    <hr>
    <p class="lead">If this is the page you are looking for:</p>
    <p>You can find the code for this project on <a href="https://github.com/dries007/links">Github</a>.</p>
    <p>There also is an API available in <a href="/api/">/api/</a>.</p>
    <?php if ($SHOW_PLUGINS) { ?>
    <p>You can use any plugin from the list below by adding it to the end of the link.<br>
        Like so: <code><?php echo $LINK_PREFIX; for ($i = 0; $i < $ID_SIZE; $i++) echo $i % 10; ?>/plugin</code></p>
    <ul>
<?php
        $dir = array_diff(scandir('plugins'), array('..', '.', 'index.php'));
        foreach($dir as $v)
        {
            if (substr($v, -strlen('.php')) !== '.php') continue;
            $v = substr($v, 0, -strlen('.php')); ?>
        <li><?php echo "<code>$v</code>: ";
            /** @noinspection PhpIncludeInspection */
            include_once "plugins/$v.php";
            ?></li>
<?php } ?>
    </ul>
<?php } ?>
</div>

<footer class="footer">
    <div class="container">
        <span class="text-muted">Copyright &copy; 2016 <a href="https://dries007.net" class="link-muted">Dries007</a></span>
    </div>
</footer>

</body>
</html>