<?php include_once "../config.inc.php" ?>
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
    <title>API</title>
</head>
<body>

<div class="container">
    <h1 class="m-t-1">Dries007's Private URL-shortener <span class="label label-info">API</span></h1>
    <?php if ($DEBUG) echo '<div class="alert alert-danger" role="alert"><strong>Danger!</strong> Debug is enabled</div>'?>
    <p>Remember that this service is not public. If you want an API key ask me.</p>
    <ul>
<?php
    $dir = array_diff(scandir('.'), array('..', '.', 'index.php'));
    foreach($dir as $v)
    {
        if (substr($v, -strlen('.php')) !== '.php') continue;
        $v = substr($v, 0, -strlen('.php')); ?>
        <li><a href="/api/<?php echo $v?>?help" class="link-muted"><code>/api/<?php echo $v?></code></a></li>
<?php } ?>
    </ul>
</div>

<footer class="footer">
    <div class="container">
        <span class="text-muted">Copyright &copy; 2016 <a href="https://dries007.net" class="link-muted">Dries007</a></span>
    </div>
</footer>

</body>
</html>